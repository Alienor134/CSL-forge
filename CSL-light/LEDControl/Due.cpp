#include "Due.h"

Due::Due()
        : timer_()
{
}

ITimer& Due::get_timer()
{
        return timer_;
}
