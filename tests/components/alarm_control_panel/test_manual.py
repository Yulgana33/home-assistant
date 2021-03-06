"""The tests for the manual Alarm Control Panel component."""
from datetime import timedelta
import unittest
from unittest.mock import patch

from homeassistant.setup import setup_component
from homeassistant.const import (
    STATE_ALARM_DISARMED, STATE_ALARM_ARMED_HOME, STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_NIGHT, STATE_ALARM_PENDING, STATE_ALARM_TRIGGERED)
from homeassistant.components import alarm_control_panel
import homeassistant.util.dt as dt_util

from tests.common import fire_time_changed, get_test_home_assistant

CODE = 'HELLO_CODE'


class TestAlarmControlPanelManual(unittest.TestCase):
    """Test the manual alarm module."""

    def setUp(self):  # pylint: disable=invalid-name
        """Setup things to be run when tests are started."""
        self.hass = get_test_home_assistant()

    def tearDown(self):  # pylint: disable=invalid-name
        """Stop down everything that was started."""
        self.hass.stop()

    def test_arm_home_no_pending(self):
        """Test arm home method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'code': CODE,
                'pending_time': 0,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_home(self.hass, CODE)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_HOME,
                         self.hass.states.get(entity_id).state)

    def test_arm_home_with_pending(self):
        """Test arm home method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'code': CODE,
                'pending_time': 1,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_home(self.hass, CODE, entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        state = self.hass.states.get(entity_id)
        assert state.attributes['post_pending_state'] == STATE_ALARM_ARMED_HOME

        future = dt_util.utcnow() + timedelta(seconds=1)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        state = self.hass.states.get(entity_id)
        assert state.state == STATE_ALARM_ARMED_HOME

    def test_arm_home_with_invalid_code(self):
        """Attempt to arm home without a valid code."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'code': CODE,
                'pending_time': 1,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_home(self.hass, CODE + '2')
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

    def test_arm_away_no_pending(self):
        """Test arm home method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'code': CODE,
                'pending_time': 0,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_away(self.hass, CODE, entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_AWAY,
                         self.hass.states.get(entity_id).state)

    def test_arm_away_with_pending(self):
        """Test arm home method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'code': CODE,
                'pending_time': 1,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_away(self.hass, CODE)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        state = self.hass.states.get(entity_id)
        assert state.attributes['post_pending_state'] == STATE_ALARM_ARMED_AWAY

        future = dt_util.utcnow() + timedelta(seconds=1)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        state = self.hass.states.get(entity_id)
        assert state.state == STATE_ALARM_ARMED_AWAY

    def test_arm_away_with_invalid_code(self):
        """Attempt to arm away without a valid code."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'code': CODE,
                'pending_time': 1,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_away(self.hass, CODE + '2')
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

    def test_arm_night_no_pending(self):
        """Test arm night method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'code': CODE,
                'pending_time': 0,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_night(self.hass, CODE)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_NIGHT,
                         self.hass.states.get(entity_id).state)

    def test_arm_night_with_pending(self):
        """Test arm night method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'code': CODE,
                'pending_time': 1,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_night(self.hass, CODE, entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        state = self.hass.states.get(entity_id)
        assert state.attributes['post_pending_state'] == \
            STATE_ALARM_ARMED_NIGHT

        future = dt_util.utcnow() + timedelta(seconds=1)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        state = self.hass.states.get(entity_id)
        assert state.state == STATE_ALARM_ARMED_NIGHT

    def test_arm_night_with_invalid_code(self):
        """Attempt to night home without a valid code."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'code': CODE,
                'pending_time': 1,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_night(self.hass, CODE + '2')
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

    def test_trigger_no_pending(self):
        """Test triggering when no pending submitted method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'trigger_time': 1,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_trigger(self.hass, entity_id=entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=60)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_TRIGGERED,
                         self.hass.states.get(entity_id).state)

    def test_trigger_with_pending(self):
        """Test arm home method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'pending_time': 2,
                'trigger_time': 3,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_trigger(self.hass)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        state = self.hass.states.get(entity_id)
        assert state.attributes['post_pending_state'] == STATE_ALARM_TRIGGERED

        future = dt_util.utcnow() + timedelta(seconds=2)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        state = self.hass.states.get(entity_id)
        assert state.state == STATE_ALARM_TRIGGERED

        future = dt_util.utcnow() + timedelta(seconds=5)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        state = self.hass.states.get(entity_id)
        assert state.state == STATE_ALARM_DISARMED

    def test_armed_home_with_specific_pending(self):
        """Test arm home method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'pending_time': 10,
                'armed_home': {
                    'pending_time': 2
                }
            }}))

        entity_id = 'alarm_control_panel.test'

        alarm_control_panel.alarm_arm_home(self.hass)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=2)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_HOME,
                         self.hass.states.get(entity_id).state)

    def test_armed_away_with_specific_pending(self):
        """Test arm home method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'pending_time': 10,
                'armed_away': {
                    'pending_time': 2
                }
            }}))

        entity_id = 'alarm_control_panel.test'

        alarm_control_panel.alarm_arm_away(self.hass)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=2)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_AWAY,
                         self.hass.states.get(entity_id).state)

    def test_armed_night_with_specific_pending(self):
        """Test arm home method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'pending_time': 10,
                'armed_night': {
                    'pending_time': 2
                }
            }}))

        entity_id = 'alarm_control_panel.test'

        alarm_control_panel.alarm_arm_night(self.hass)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=2)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_NIGHT,
                         self.hass.states.get(entity_id).state)

    def test_trigger_with_specific_pending(self):
        """Test arm home method."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'pending_time': 10,
                'triggered': {
                    'pending_time': 2
                },
                'trigger_time': 3,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        alarm_control_panel.alarm_trigger(self.hass)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=2)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_TRIGGERED,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=5)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

    def test_trigger_with_disarm_after_trigger(self):
        """Test disarm after trigger."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'trigger_time': 5,
                'pending_time': 0,
                'disarm_after_trigger': True
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_trigger(self.hass, entity_id=entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_TRIGGERED,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=5)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

    def test_trigger_with_no_disarm_after_trigger(self):
        """Test disarm after trigger."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'trigger_time': 5,
                'pending_time': 0,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_away(self.hass, CODE, entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_AWAY,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_trigger(self.hass, entity_id=entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_TRIGGERED,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=5)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_AWAY,
                         self.hass.states.get(entity_id).state)

    def test_back_to_back_trigger_with_no_disarm_after_trigger(self):
        """Test disarm after trigger."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'trigger_time': 5,
                'pending_time': 0,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_arm_away(self.hass, CODE, entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_AWAY,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_trigger(self.hass, entity_id=entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_TRIGGERED,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=5)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_AWAY,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_trigger(self.hass, entity_id=entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_TRIGGERED,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=5)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_ARMED_AWAY,
                         self.hass.states.get(entity_id).state)

    def test_disarm_while_pending_trigger(self):
        """Test disarming while pending state."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'trigger_time': 5,
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_trigger(self.hass)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_disarm(self.hass, entity_id=entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=5)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

    def test_disarm_during_trigger_with_invalid_code(self):
        """Test disarming while code is invalid."""
        self.assertTrue(setup_component(
            self.hass, alarm_control_panel.DOMAIN,
            {'alarm_control_panel': {
                'platform': 'manual',
                'name': 'test',
                'pending_time': 5,
                'code': CODE + '2',
                'disarm_after_trigger': False
            }}))

        entity_id = 'alarm_control_panel.test'

        self.assertEqual(STATE_ALARM_DISARMED,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_trigger(self.hass)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        alarm_control_panel.alarm_disarm(self.hass, entity_id=entity_id)
        self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_PENDING,
                         self.hass.states.get(entity_id).state)

        future = dt_util.utcnow() + timedelta(seconds=5)
        with patch(('homeassistant.components.alarm_control_panel.manual.'
                    'dt_util.utcnow'), return_value=future):
            fire_time_changed(self.hass, future)
            self.hass.block_till_done()

        self.assertEqual(STATE_ALARM_TRIGGERED,
                         self.hass.states.get(entity_id).state)
