/*
  
  Copyright (C) 2022 Sony Computer Science Laboratories
  
  Author(s) Peter Hanappe, Douglas Boari, Aliénor Lahlou
  
  free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see
  <http://www.gnu.org/licenses/>.
  
 */
#include <ArduinoSerial.h>
#include <RomiSerial.h>
#include <RomiSerialErrors.h>
#include <stdint.h>
#include "AnalogMeasure.h"
#include "DigitalPulse.h"
#include "PrimaryDigitalPulse.h"
#include "ActivityManager.h"
#include "BoardFactory.h"
#include "ITimer.h"
#include "IBoard.h"
#include "EndSwitch.h"
#include "Relay.h"

using namespace romiserial;

void send_info(IRomiSerial *romiSerial, int16_t *args, const char *string_arg);
void handle_add_analogue_measure(IRomiSerial *romiSerial, int16_t *args,
                                 const char *string_arg);
void handle_add_digital_pulse(IRomiSerial *romiSerial, int16_t *args,
                              const char *string_arg);
void handle_add_primary_digital_pulse(IRomiSerial *romiSerial, int16_t *args,
                                      const char *string_arg);
void handle_stop_measurements(IRomiSerial *romiSerial, int16_t *args,
                              const char *string_arg);
void handle_start_mesurements(IRomiSerial *romiSerial, int16_t *args,
                              const char *string_arg);
void handle_relay_pin(IRomiSerial *romiSerial, int16_t *args, const char *string_arg);
void handle_is_done(IRomiSerial *romiSerial, int16_t *args, const char *string_arg);
void handle_reset(IRomiSerial *romiSerial, int16_t *args, const char *string_arg);

const static MessageHandler handlers[] = {
        { 'a', 9, false, handle_add_analogue_measure },
        { 'd', 9, false, handle_add_digital_pulse },
        { 'm', 9, false, handle_add_primary_digital_pulse },
        { 'b', 2, false, handle_start_mesurements },
        { 'e', 0, false, handle_stop_measurements },
        { 'r', 0, false, handle_reset },
        { 'R', 1, false, handle_relay_pin },
        { 'E', 0, false, handle_is_done },
        { '?', 0, false, send_info },
};

static int kMaxActivitiesCode = 1;
static int kBadStartCode = 2;
static int kBadPeriodCode = 3;
static int kBadDurationCode = 4;

static char *kMaxActivitiesMessage = "Too many activities";
static char *kBadStartMessage = "Bad start";
static char *kBadPeriodMessage = "Bad period";
static char *kBadDurationMessage = "Bad duration";

#if defined(ARDUINO_SAM_DUE)
ArduinoSerial serial(SerialUSB);
#else
ArduinoSerial serial(Serial);
#endif

RomiSerial romiSerial(serial, serial, handlers, sizeof(handlers) / sizeof(MessageHandler));
ActivityManager activityManager;
Relay *relay = nullptr;
EndSwitch *endSwitch = nullptr;

extern volatile int32_t timer_interrupts_;

void setup()
{
#if defined(ARDUINO_SAM_DUE)
        SerialUSB.begin(0);
        while(!SerialUSB)
                ;
#else
        Serial.begin(115200);
        while (!Serial)
                ;
#endif

        IBoard& board = BoardFactory::get();
        ITimer& timer = board.get_timer();
        timer.init();

        relay = new Relay();
        endSwitch = new EndSwitch();
        activityManager.addActivity(relay);
        activityManager.addActivity(endSwitch);
        
        activityManager.addDigitalPulse(2, 0, 4, 10, 0);
        //activityManager.addDigitalPulse(3, 4, 1, 10, 0);
        relay->setPin(3);
        endSwitch->setDuration(2000);
        timer.start(activityManager.getActivities(),
                    activityManager.countActivities());
}

void loop()
{
        romiSerial.handle_input();
        delay(10);
}

void send_info(IRomiSerial *romiSerial, int16_t *args, const char *string_arg)
{
        romiSerial->send("[\"LightControl\",\"0.1\"]"); 
}
  
void handle_add_analogue_measure(IRomiSerial *romiSerial, int16_t *args,
                                 const char *string_arg)
{        
        int8_t pin = (uint8_t) args[0];
        int32_t start_delay = (int32_t) args[1] * 1000 + args[2];
        int32_t duration = (int32_t) args[3] * 1000 + args[4];
        int32_t period = (int32_t) args[5] * 1000 + args[6];
        int8_t secondary = (uint8_t) args[7];

        if (start_delay < 0)
                romiSerial->send_error(kBadStartCode, kBadStartMessage);
        else if (period <= 0)
                romiSerial->send_error(kBadPeriodCode, kBadPeriodMessage);
        else if (duration < 0 || duration > period)
                romiSerial->send_error(kBadDurationCode, kBadDurationMessage);
        else if (activityManager.addAnalogueMeasure(pin, start_delay, duration,
                                                      period, secondary))
                romiSerial->send_ok();
        else
                romiSerial->send_error(kMaxActivitiesCode, kMaxActivitiesMessage);
}

void handle_add_digital_pulse(IRomiSerial *romiSerial, int16_t *args,
                              const char *string_arg)
{
        int8_t pin = (uint8_t) args[0];
        int32_t start_delay = (int32_t) args[1] * 1000 + args[2];
        int32_t duration = (int32_t) args[3] * 1000 + args[4];
        int32_t period = (int32_t) args[5] * 1000 + args[6];
        int8_t secondary = (uint8_t) args[7];
        int16_t dummy = args[8];
    
        if (start_delay < 0)
                romiSerial->send_error(kBadStartCode, kBadStartMessage);
        else if (period <= 0)
                romiSerial->send_error(kBadPeriodCode, kBadPeriodMessage);
        else if (duration < 0 || duration > period)
                romiSerial->send_error(kBadDurationCode, kBadDurationMessage);
        else if (activityManager.addDigitalPulse(pin, start_delay, duration,
                                                 period, secondary /*, args[8]*/))
                romiSerial->send_ok(); 
        else
                romiSerial->send_error(kMaxActivitiesCode, kMaxActivitiesMessage);
}

void handle_add_primary_digital_pulse(IRomiSerial *romiSerial, int16_t *args,
                                      const char *string_arg)
{
        int8_t pin = (uint8_t) args[0];
        int32_t start_delay = (int32_t) args[1] * 1000 + args[2];
        int32_t duration = (int32_t) args[3] * 1000 + args[4];
        int32_t period = (int32_t) args[5] * 1000 + args[6];
        int8_t secondary = (uint8_t) args[7];
        int16_t dummy = args[8];
        
        if (start_delay < 0)
                romiSerial->send_error(kBadStartCode, kBadStartMessage);
        else if (period <= 0)
                romiSerial->send_error(kBadPeriodCode, kBadPeriodMessage);
        else if (duration < 0 || duration > period)
                romiSerial->send_error(kBadDurationCode, kBadDurationMessage);
        else if (activityManager.addPrimaryDigitalPulse(pin, start_delay, duration,
                                                   period, secondary/*, args[8]*/)) 
                romiSerial->send_ok();
        else
                romiSerial->send_error(kMaxActivitiesCode, kMaxActivitiesMessage);
}

void handle_start_mesurements(IRomiSerial *romiSerial, int16_t *args,
                              const char *string_arg)
{
        int32_t duration = (int32_t) args[0] * 1000 + args[1];
        if (duration > 0)
                endSwitch->setDuration(duration);
        
        IBoard& board = BoardFactory::get();
        ITimer& timer = board.get_timer();
        timer.start(activityManager.getActivities(),
                    activityManager.countActivities());
        
        romiSerial->send_ok();
}

void handle_stop_measurements(IRomiSerial *romiSerial, int16_t *args,
                              const char *string_arg)
{
        IBoard& board = BoardFactory::get();
        ITimer& timer = board.get_timer();
        timer.stop();
        
        romiSerial->send_ok();
}

void handle_relay_pin(IRomiSerial *romiSerial, int16_t *args, const char *string_arg)
{
        relay->setPin(args[0]);
        romiSerial->send_ok();
}

void handle_is_done(IRomiSerial *romiSerial, int16_t *args, const char *string_arg)
{
        if (endSwitch->isDone()) {
                romiSerial->send("[0,1]"); 
        } else {
                romiSerial->send("[0,0]"); 
        }
}

void handle_reset(IRomiSerial *romiSerial, int16_t *args, const char *string_arg)
{
        romiSerial->send_ok();
}
