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

#include "Arduino.h"
#include "AnalogMeasure.h"
#include "DigitalPulse.h"
#include "PrimaryDigitalPulse.h"
#include "ActivityManager.h"

ActivityManager::ActivityManager() : current_number_activities(0)
{
        for (uint8_t index = 0; index < MAX_ACTIVITIES; index++) {
                activities[index] = nullptr;
        }
}

ActivityManager::~ActivityManager()
{
        for (uint8_t index = 0; index < current_number_activities; index++) {
                delete activities[index];
                activities[index] = nullptr;
        }
}

bool ActivityManager::addActivity(IActivity *newactivity)
{
        bool retval = false;
        if (newactivity != nullptr) {
                activities[current_number_activities++] = newactivity;
                retval = true;
        }
        return retval;
}

bool ActivityManager::addDigitalPulse(int8_t pin, int32_t start_delay_ms,
                                      int32_t duration, int32_t period,
                                      int8_t secondary// , int32_t analog_value
        )
{
        bool retval = false;

        if (current_number_activities < MAX_ACTIVITIES) {
                auto newactivity = new DigitalPulse(pin, start_delay_ms, period, duration,
                                                    secondary
                                                    /*, analog_value*/);
                retval = addActivity(newactivity);
        }
        return retval;
}

bool ActivityManager::addPrimaryDigitalPulse(int8_t pin, int32_t start_delay_ms,
                                             int32_t duration, int32_t period,
                                             int8_t secondary/*, int32_t analog_value*/)
{
        bool retval = false;
        int8_t current_number_secondarys = 0;
        if (current_number_activities < MAX_ACTIVITIES) {
                auto newactivity = new PrimaryDigitalPulse(pin, start_delay_ms, period,
                                                           duration, secondary
                                                           /*,analog_value*/);
                retval = addActivity(newactivity);
                for (int i = 0; i < current_number_activities;  i++) {
                        if (activities[i]->isSecondary()) {
                                newactivity->addSecondary(activities[i]);
                        }
                }        
        }
        return retval;
}

bool ActivityManager::addAnalogueMeasure(int8_t pin, int32_t start_delay_ms,
                                         int32_t duration, int32_t period,
                                         int8_t secondary)
{
        bool retval = false;
        if (current_number_activities < MAX_ACTIVITIES){
                auto newactivity = new AnalogMeasure(pin, start_delay_ms, duration,
                                                     period, secondary);
                retval = addActivity(newactivity);
        }
        return retval;
}

IActivity **ActivityManager::getActivities()
{
        return activities;
}

uint8_t ActivityManager::countActivities()
{
        return current_number_activities;
}
