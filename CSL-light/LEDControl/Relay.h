#ifndef __Relay_h
#define __Relay_h

#include "IActivity.h"

class Relay : public IActivity
{
protected:
        int8_t pin_;
        
public:
        Relay() : pin_(-1) {
        }
        
        ~Relay() override = default;


        void setPin(int8_t pin) {
                off();
                pin_ = pin;
                pinMode(pin_, OUTPUT);                
        }
        
        void start() override {
                on();
        }
                
        void update(int32_t ms) override {
        }
                
        void stop() override {
                off();
        }
        
        void on() override {
                if (pin_ > 0)
                        digitalWrite(pin_, HIGH);
        }
        
        void off() override {
                if (pin_ > 0)
                        digitalWrite(pin_, LOW);
        }
        
        bool isOn() override {
                return pin_ > 0;
        }
        
        uint8_t isSecondary() {
                return 0;
        }
};

#endif // __Relay_h
