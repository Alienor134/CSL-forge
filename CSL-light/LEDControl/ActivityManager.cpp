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
#include "ActivityManager.h"

ActivityManager::ActivityManager() : current_number_activities(0)
{
    for (uint8_t index = 0; index < MAX_ACTIVITIES; index++)
    {
        activities[index] = nullptr;
    }
}

ActivityManager::~ActivityManager()
{
    for (uint8_t index = 0; index < current_number_activities; index++)
    {
        delete activities[index];
        activities[index] = nullptr;
    }
}

bool ActivityManager::AddActivity(PeriodicActivity *newactivity)
{
    bool retval = false;
    if (newactivity != nullptr)
    {
        activities[current_number_activities++] = newactivity;
        retval = true;
    }
    return retval;
}


bool ActivityManager::AddDigitalPulse(int32_t pin, int32_t start_delay_ms, int32_t duration, int32_t period, int32_t secondary, int32_t analog_value)
{
    bool retval = false;

    if (current_number_activities < MAX_ACTIVITIES)
    {
        auto newactivity = new DigitalPulse(pin, start_delay_ms, duration, period, secondary, analog_value);
        retval = AddActivity(newactivity);
    }
    return retval;
}

bool ActivityManager::AddprimaryDigitalPulse(int32_t pin, int32_t start_delay_ms, int32_t duration, int32_t period, int32_t secondary, int32_t analog_value)
{
    bool retval = false;
    int8_t current_number_secondarys = 0;
    if (current_number_activities < MAX_ACTIVITIES)
    {
        auto newactivity = new primaryDigitalPulse(pin, start_delay_ms, duration, period, secondary, analog_value);
        retval = AddActivity(newactivity);
        for (int i = 0; i < current_number_activities;  i++)
        {
            if(activities[i]->is_secondary()>0)
            {
                newactivity->Addsecondary(activities[i]);
            }
        }        
    }
    return retval;
}

bool ActivityManager::AddAnalogueMeasure(int32_t pin, int32_t start_delay_ms, int32_t duration, int32_t period, int32_t secondary)
{
        bool retval = false;
        if (current_number_activities < MAX_ACTIVITIES)
        {
            auto newactivity = new AnalogMeasure(pin, start_delay_ms, duration, period, secondary);
            retval = AddActivity(newactivity);
        }
        return retval;
}

PeriodicActivity **ActivityManager::Activities()
{
    return activities;
}

uint8_t ActivityManager::NumberActivities()
{
    return current_number_activities;
}

void ActivityManager::enable(bool enabled)
{
    for (uint8_t index = 0; index < current_number_activities; index++)
    {
        if (enabled)
            activities[index]->enable();
        else
            activities[index]->disable();
    }
}
