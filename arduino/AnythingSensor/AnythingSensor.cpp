#include "AnythingSensor.h"

 AnythingSensor* _instance = nullptr;

AnythingSensor::AnythingSensor()
{
    _instance = this;
}

bool AnythingSensor::begin()
{
    // Create a temporary buffer with size 1 for reading config information
    AnythingSensor::buffer = new byte[4];
    AnythingSensor::bufferLength = 4;
    AnythingSensor::buffer[0] = 0;
    AnythingSensor::buffer[1] = 0;
    AnythingSensor::buffer[2] = 0;
    AnythingSensor::buffer[3] = 0;


    // Iniitliaze variables for ISR
    AnythingSensor::pos = 0;
    AnythingSensor::dataAvailable = false;

    spiInit();

    commInit();

    dataInit();

    return true;
}

void AnythingSensor::spiInit()
{
    // Set our commState to the INIT state
    commState = INIT;

    // Set the signal pin to output mode
    pinMode(signalPin, OUTPUT);
    digitalWrite(signalPin, LOW);

    // Enable SPI in slave mode
    // Set Master In Slave Out as output
    pinMode(MISO, OUTPUT);


    // Set SPDR to 0x00
    SPDR = 0x00;

    // turn on SPI in slave mode
    SPCR |= _BV(SPE);

    // turn on interrupt for
    SPCR |= _BV(SPIE);
}

void AnythingSensor::commInit()
{
    // Booleans to store the state of initialization
    bool initCompleted = false;
    bool startMessagedReceived = false;
    while(!initCompleted)
    {
        commState = INIT; // Ensure comm state is in init

        // First step of initialization, receive 4 0xFF messages from the Anything Sensor
        startMessagedReceived = false;
        while(!startMessagedReceived)
        {
            if(AnythingSensor::dataAvailable)
            {
                // Check that all of the data in the buffer is 0xFF
                if(AnythingSensor::buffer[0] == 0xFF &&
                    AnythingSensor::buffer[1] == 0xFF &&
                    AnythingSensor::buffer[2] == 0xFF &&
                    AnythingSensor::buffer[3] == 0xFF)
                {
                    startMessagedReceived = true;
                    dataAvailable = false;
                }
                else
                {
                    // Reset buffer to wait for new group of start bits
                    AnythingSensor::buffer[0] = 0;
                    AnythingSensor::buffer[1] = 0;
                    AnythingSensor::buffer[2] = 0;
                    AnythingSensor::buffer[3] = 0;
                    AnythingSensor::dataAvailable = false;
                }
            }
        }

        Serial.println("Received starting message");

        // Second step involves sending two things to the Anything Sensor
        // First, a digital HIGH is sent on the signal pin to signal receipt of message
        // The Anything Sensor will request data transfer. In that transfer, 0x01 must
        // be sent by the slave

        Serial.println("Requesting sample data");
        // Write 0x01 to SPI output buffer to send to Anything Sensor
        requestData();

        // Check that all of the data in the buffer is 0x00
        // If it is, the initialization has been completed successfully
        // Else, we return to the beginning of the init process to try again
        if(AnythingSensor::buffer[0] == 0x00 &&
            AnythingSensor::buffer[1] == 0x00 &&
            AnythingSensor::buffer[2] == 0x00 &&
            AnythingSensor::buffer[3] == 0x00)
        {
            AnythingSensor::dataAvailable = false;

            initCompleted = true;
            Serial.println("Successfully Initialized");
        }
    }
    // Wait 1 second after init process
    delay(500);
}

void AnythingSensor::requestData()
{
    // Write high to signal pin to signal ready to receive data
    digitalWrite(signalPin, HIGH);

    // Wait for data to be received from AnythingSensor
    while (!dataAvailable)
    { }

    dataAvailable = false;

    digitalWrite(signalPin, LOW);
}

void AnythingSensor::dataInit()
{
    requestData();

    Serial.print("Data initialized ");
    Serial.print(buffer[0]);
    Serial.print(" ");
    Serial.print(buffer[1]);
    Serial.print(" ");
    Serial.print(buffer[2]);
    Serial.print(" ");
    Serial.print(buffer[3]);
    Serial.print(" ");

    // We have received the new data from the Anything Sensor
    // This data stores the data type and length of the data
    // buffer[0] - datatype: currently only float is supported
    // buffer[1] - length of the data
    // buffer[2] - Unused
    // buffer[3] - Unused

    // Create a data array to store the data from the Anything Sensor
    dataLength = buffer[1];
    data = new float[dataLength];
    float test = 0.0;
    data[0] = 0;

    // Disable SPI interrupt while we resize buffer
    SPCR &= ~(_BV(SPIE));

    // Resize the buffer to the correct size for the streaming data
    delete[] buffer;
    bufferLength = 4*dataLength;
    buffer = new byte[bufferLength];

    // Re-enable SPI interrupt
    SPCR |= _BV(SPIE);
    Serial.println(dataLength);
}

bool AnythingSensor::read()
{
    requestData();

    memcpy(data, buffer, bufferLength);
}


void AnythingSensor::_isr()
{
    switch(commState)
    {
    case WAITING_FOR_HEADER:
    {
        byte header = SPDR;

        if(header == 0x10) // Heartbeat header, do nothing
        { }
        else if(header == 0x20) // Message header, switch to receiving message
        {
            //Serial.println("Received Message header");
            commState = RECEIVING_MESSAGE;
        }
        else if(header == 0x30) // Config header, switch to receiving config state
        {
            // Reset heartbeat counter every time we receive config header
            // TODO This is a temporary, hacky solution
            // We are using this as a way to validate that both devices are in comms init
            // Currently, if the Arduino is requesting data while the Coral is in init mode,
            // the coral will interpret the data from the Arduino as the init sequence
            // Therefore, we need to have a different sequence that the Arduino sends as the heartbeat
            // than normal. Therefore, we make the heartbeat decrement instead of increment during the
            // init period
            // We need to add functionality such that the arduino recognizes the coral is in comm init
            // and resets its own comms
            commState = RECEIVING_CONFIG;
        }
        // else if(header == 0xFF) // Reset header, we need to reset comms with anything sensor
        // {
        //     commState = INIT;
        // }

        break;
    }
    default: // This is used for the INIT, RECEIVING_CONFIG, or RECEIVING_MESSAGE states
    {
        AnythingSensor::buffer[pos] = SPDR;

        // Check if we've reached end of buffer
        // If at the end of buffer, we have received all of the data in this packet
        pos++;
        if(pos == bufferLength)
        {
            // State that new data available in the buffer
            dataAvailable = true;

            // Reset the position in the buffer to the beginning
            pos = 0;

            // We will always transition to the WAITING_FOR_HEADER STATE
            // after a message is received
            commState = WAITING_FOR_HEADER;
        }
    }
    }
    // Set the output register to the heartbeat counter and increment the heartbeat counter
    SPDR = heartbeatCounter;
    if(commState != INIT)
        heartbeatCounter++;
    else
        heartbeatCounter--;
}

int AnythingSensor::length()
{
    return dataLength;
}

float AnythingSensor::get(int i)
{
    return data[i];
}

// SPI interrupt routine
 ISR (SPI_STC_vect)
 {
     _instance -> _isr();
 }
