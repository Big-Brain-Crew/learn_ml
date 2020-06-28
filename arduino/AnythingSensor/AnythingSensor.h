#include "Arduino.h"
//#include "AnythingSensorData.h"

enum SPIState
{
    INIT,
    WAITING_FOR_HEADER,
    RECEIVING_CONFIG,
    RECEIVING_MESSAGE
};


class AnythingSensor
{
    private:
        // Stores the sensor data collected from the Anything Sensor
        // The memory for this is dynamically allocated when the communication is established
        // because the Anything Sensor communicates the data size to the Arduino
        volatile byte* buffer;
        volatile int bufferLength;

        // Position in the buffer the ISR is currently writing to
        volatile int pos;
        volatile bool dataAvailable;

        volatile byte heartbeatCounter = 0xFF;



        // Stores the data after it is converted to floating point
        float* data;

        // Stores the length of the buffer
        int dataLength;

        // This is the pin that the Arduino will send a signal to the
        // coral board over.
        int signalPin = 9;

        volatile SPIState commState;

        void spiInit();

        void commInit();

        void dataInit();

        void requestData();

    public:
        // Default constructor
        AnythingSensor();

        bool begin();

        bool end();

        bool read();

        int length();

        void _isr();

        float get(int i);
};
