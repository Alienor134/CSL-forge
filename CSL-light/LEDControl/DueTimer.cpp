#if defined(ARDUINO_SAM_DUE)

#include <Arduino.h>
#include "DueTimer.h"

volatile bool running_ = false;
volatile int32_t current_time_ms_ = 0;
volatile int32_t timer_interrupts_ = 0;
IActivity **activities_ = nullptr;
int num_activities_ = 0;

const uint16_t kBufferLength = 20; // 2 channels x 10 samples
const uint8_t kNumberOfBuffers = 4;
const uint8_t kBufferModuloMask = kNumberOfBuffers - 1;
volatile uint16_t adc_buffer[kNumberOfBuffers][kBufferLength];
volatile uint8_t current_adc_write_buffer;
volatile uint8_t current_adc_read_buffer;

uint16_t dac_buffer[kNumberOfBuffers][kBufferLength];
volatile uint8_t current_dac_buffer = 0;

static void setup_adc();
static void setup_dac();
static void setup_adc_timer();
static void setup_dac_timer();     

static void start_activities();
static void stop_activities();
static inline void update_activities(int32_t ms);

DueTimer::DueTimer()
{
}

void DueTimer::init()
{
        SerialUSB.println("DueTimer::DueTimer");
        noInterrupts();
        setup_adc();
        setup_dac();
        setup_adc_timer();
        setup_dac_timer();     
        interrupts(); 
}

void DueTimer::start(IActivity **a, int n)
{
        running_ = false;
        activities_ = a;
        num_activities_ = n;
        current_time_ms_ = 0;
        start_activities();
        running_ = true;
}

void DueTimer::stop()
{
        stop_activities();
        running_ = false;
        num_activities_ = 0;
        activities_ = nullptr;
}

bool DueTimer::isActive()
{
        return running_;
}

// FIXME
static void start_activities()
{
        for (int i = 0; i < num_activities_; i++) {
                activities_[i]->start();
        }
}

// FIXME
static void stop_activities()
{
        for (int i = 0; i < num_activities_; i++) {
                activities_[i]->stop();
        }
}

// FIXME
static inline void update_activities(int32_t ms)
{
        for (int i = 0; i < num_activities_; i++) {
                if (!activities_[i]->isSecondary())
                        activities_[i]->update(ms);
        }
        for (int i = 0; i < num_activities_; i++) {
                if (activities_[i]->isSecondary())
                        activities_[i]->update(ms);
        }
}

static inline void call_activities()
{
        if (running_) {
                update_activities(current_time_ms_);
        }
}

static void setup_adc()
{
        // ADC power ON
        PMC->PMC_PCER1 |= PMC_PCER1_PID37;

        // Reset ADC
        ADC->ADC_CR = ADC_CR_SWRST;

        // Hardware trigger select
        ADC->ADC_MR |=  ADC_MR_TRGEN_EN
                | ADC_MR_TRGSEL_ADC_TRIG2 // Trigger by TIOA1
                | ADC_MR_PRESCAL(1);
        
        // For frequencies > 500 KHz
        // ADC->ADC_ACR = ADC_ACR_IBCTL(0b01);

        ADC->ADC_IDR = ~ADC_IDR_ENDRX;
        
        // End Of Conversion interrupt enable for channel 7
        ADC->ADC_IER = ADC_IER_ENDRX;

        //NVIC_SetPriority(ADC_IRQn, 0xFF);
        
        // Enable ADC interrupt
        NVIC_EnableIRQ(ADC_IRQn);

        // Enable Channels 7 = A0 and 6 = A1; Trigger frequency is
        // multiplied by 2
        ADC->ADC_CHER = ADC_CHER_CH6 | ADC_CHER_CH7;

        // The sampling frequency for 1 channel times the number of channels !!

        // PDC/DMA  buffer filling sequence

        // DMA buffer - First one will be buffer[1]
        ADC->ADC_RPR = (uint32_t) adc_buffer[2];
        ADC->ADC_RCR = kBufferLength;

        // Next DMA buffer
        ADC->ADC_RNPR = (uint32_t) adc_buffer[3];
        ADC->ADC_RNCR = kBufferLength;
        current_adc_write_buffer = 3;
        current_adc_read_buffer = 3;
        
        // Enable PDC Receiver channel request
        ADC->ADC_PTCR |= ADC_PTCR_RXTEN;
        //ADC->ADC_CR = ADC_CR_START;
}

/* Interrupt handler for ADC PDC/DMA */
void ADC_Handler()
{
        
        //if ( ADC->ADC_ISR & ADC_ISR_ENDRX) { // Useless because the only one
        current_adc_write_buffer = (current_adc_write_buffer + 1) & kBufferModuloMask;
        ADC->ADC_RNPR = (uint32_t) adc_buffer[current_adc_write_buffer];
        ADC->ADC_RNCR = kBufferLength;

        call_activities();
        current_time_ms_++;
        
        timer_interrupts_++;
        
        /*************************************************/
        // For debugging only
        // if ((timer_interrupts_ % 1000) == 0) { //84000000/8/1050/2/10  = 500... ?
        //         PIOB->PIO_ODSR ^= PIO_ODSR_P27;  // Toggle LED_BUILTIN every 1 Hz
        // }
        /*************************************************/
        // }
}

/* Configure adc_setup function */
static void setup_dac()
{
        // DACC power ON
        PMC->PMC_PCER1 = PMC_PCER1_PID38;

        // Reset DACC
        DACC->DACC_CR = DACC_CR_SWRST;

        // Hardware trigger select
        DACC->DACC_MR = DACC_MR_TRGEN_EN
                | DACC_MR_TRGSEL(0b011)  // Trigger by TIOA2
                | DACC_MR_TAG_EN         // Output on DAC0 and DAC1
                | DACC_MR_WORD_HALF
                | DACC_MR_REFRESH (1)
                | DACC_MR_STARTUP_8
                | DACC_MR_MAXS;

        DACC->DACC_ACR = DACC_ACR_IBCTLCH0(0b11) // 0b10
                | DACC_ACR_IBCTLCH1(0b11) // 0b10
                | DACC_ACR_IBCTLDACCORE(0b01);

        DACC->DACC_IDR = ~DACC_IDR_ENDTX;
        DACC->DACC_IER = DACC_IER_ENDTX;    // TXBUFE works too !!!
        //NVIC_SetPriority(DACC_IRQn, 0xFF);
        NVIC_EnableIRQ(DACC_IRQn);

        // enable channels 1 = DAC1 and 0 = DAC0
        DACC->DACC_CHER = DACC_CHER_CH0 | DACC_CHER_CH1;

        // Configure PDC/DMA  for DAC
        // DMA buffer

        memset(dac_buffer[0], 0, kBufferLength * sizeof(uint16_t));
        memset(dac_buffer[1], 0, kBufferLength * sizeof(uint16_t));
        
        DACC->DACC_TPR = (uint32_t) dac_buffer[0];
        DACC->DACC_TCR = kBufferLength;
        
        // Next DMA buffer
        DACC->DACC_TNPR = (uint32_t) dac_buffer[1];
        DACC->DACC_TNCR =  kBufferLength;
        current_dac_buffer = 1;
        
        // Enable PDC Transmit channel request
        DACC->DACC_PTCR = DACC_PTCR_TXTEN;
}

/* Call back function for DAC PDC/DMA */
void DACC_Handler()
{
        current_dac_buffer = (current_dac_buffer + 1) % kNumberOfBuffers;
        //wavetable.generate(dac_buffer[current_dac_buffer], kBufferLength);
        
        DACC->DACC_TNPR = (uint32_t) dac_buffer[current_dac_buffer];
        DACC->DACC_TNCR = kBufferLength;
}

/* Timer Counter 0 Channel 1 to generate PWM pulses thru TIOA1 for
 * ADC */
static void setup_adc_timer()
{
        // TC1 power ON : Timer Counter 0 channel 1 IS TC1
        PMC->PMC_PCER0 |= PMC_PCER0_PID28;
        
        // MCK/8, clk on rising edge
        TC0->TC_CHANNEL[1].TC_CMR = TC_CMR_TCCLKS_TIMER_CLOCK2
                | TC_CMR_WAVE               // Waveform mode
                | TC_CMR_WAVSEL_UP_RC       // UP mode with automatic trigger on RC Compare
                | TC_CMR_ACPA_CLEAR         // Clear TIOA1 on RA compare match
                | TC_CMR_ACPC_SET;          // Set TIOA1 on RC compare match

        // Frequency = (Mck/8)/TC_RC  Hz = 44.1 Hz
        TC0->TC_CHANNEL[1].TC_RC = 1050;
        // Any Duty cycle in between 1 and TC_RC
        TC0->TC_CHANNEL[1].TC_RA = 40;
        // TC1 enable
        TC0->TC_CHANNEL[1].TC_CCR = TC_CCR_CLKEN;
}


/* Timer Counter 0 Channel 2 to generate PWM pulses thru TIOA2 for
 * DACC */
static void setup_dac_timer()
{
        // TC2 power ON : Timer Counter 0 channel 2 IS TC2
        PMC->PMC_PCER0 |= PMC_PCER0_PID29;

        // MCK/8, clk on rising edge
        TC0->TC_CHANNEL[2].TC_CMR = TC_CMR_TCCLKS_TIMER_CLOCK2
                | TC_CMR_WAVE               // Waveform mode
                | TC_CMR_WAVSEL_UP_RC       // UP mode with automatic trigger on RC Compare
                | TC_CMR_ACPA_CLEAR         // Clear TIOA2 on RA compare match
                | TC_CMR_ACPC_SET;          // Set TIOA2 on RC compare match

        // Frequency = (Mck/8)/TC_RC  Hz = 88.2 Hz
        TC0->TC_CHANNEL[2].TC_RC = 119;
        // Any Duty cycle in between 1 and TC_RC
        TC0->TC_CHANNEL[2].TC_RA = 20;

        // TC2 enable
        TC0->TC_CHANNEL[2].TC_CCR = TC_CCR_CLKEN;
        // Synchro TC1 and TC2
        TC0->TC_BCR = TC_BCR_SYNC;
}

#endif // if ARDUINO_SAM_DUE
