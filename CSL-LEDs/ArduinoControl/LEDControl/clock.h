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
 
#include <avr/io.h>
#include <avr/interrupt.h>
#include "PeriodicActivity.h"

#ifndef _CLOCK_H_
#define _CLOCK_H_

void clock_init();

void clock_register_activities(PeriodicActivity **activities, int num_activities);

#define clock_run()                                          \
        {                                                               \
                /* Initialize counter */                                \
                TCNT1 = 0;                                              \
                /* Enable Timer1 */                                     \
                TIMSK1 |= (1 << OCIE1A);                                \
        }

#define clock_pause()                                         \
        {                                                               \
                /* Disable Timer1 interrupt */                          \
                TIMSK1 &= ~(1 << OCIE1A);                               \
        }

#endif // _CLOCK_H_
