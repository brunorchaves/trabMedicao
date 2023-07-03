const int N = 4;          //Number of channels
const int tam = 150;      //Size of data buffers

bool sendStatus = false;  //Flag to start data processing
int dataVector[N][tam];   //Data vectors for each channel

//----------------------------
//Initialization
void setup()
{
    //Set serial port configuration and establish communication
  Serial.begin(115200);

    //Configure the ADC pins
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);

  //---------- Configure the ADC --------------------------------
    //Configure the ADC mux
  ADMUX = 0x40;    //MUX[3:0]=0000 -> select analog channel 0, 
                   //ADLAR=0 -> the ADC results are right adjusted
                   //REFS[1:0]=01, set voltage reference do AVcc

    //Configure the ADC prescaler and enable interrupts
  ADCSRA = 0x08 | 0x20 | 0x06;    //ADIE=1, enable ADC interrupts
                                  //ADATE=1, enable auto-trigger
                                  //ADPS[2:0]=110, set prescaler to 64 -> ADC_clk = 16e6/64 = 250kHz  

    //Configure the ADC trigger source
  ADCSRB = 0x03;    //ACME=0, disable analog comparator multiplexer
                    //ADTS[2:0]=011 -> trigger source = Timer/Counter0 compare match A
        
    //Disable the ADC digital input buffers
  DIDR0 = 0xFF;

  //-------- Configure the timer/counter 0 --------------------------
    //ATENÇÃO: a ordem dos comandos altera o comportamento do sistema, 
    //portanto procure manter a definida abaixo.
  TCCR0A = 0x02;    //COM0A[1:0] = 00, COM0B[1:0] = 00 -> normal port operation, OC0A, OC0B disconnected.
                    //WGM0[2:0] = 010 -> CTC mode (clear timer/counter on compare)  
  TCCR0B = 0x00;    //FOC0A, FOC0B = 0 -> force output compare A, B = 0
                    //CS0[2:0] = 000 -> no clock source (timer/counter stopped)
  TCNT0 = 0;        //Reset the counter 0     
  OCR0A = 16;       //Set the compare register A
  OCR0B = 0;        //Reset the compare register B      
  TIMSK0 = 0x02;    //OCIE0A = 1 -> timer/counter 0 output compare A match interrupt enable.        

  //--------- Start acquisition ------------------------------------
    //Enable global interrupts
  SREG |= 0x80;     //Enable global interrupts
    //Enable the AD converter
  ADCSRA |= 0x80;   //ADEN=1, enable AD converter
    //Start the timer
  TCCR0B = 0x03;    //CS0[2:0] = 011 -> clkIO/64 = 250kHz
}

//-----------------------------
//ADC interrupt service routine
ISR(ADC_vect)
{
  int sample, CH;
  static int counter = 0;          //Controls the number of samples
  
      //Read the latest sample
  sample = ADCL;       //Read the lower byte
  sample += ADCH<<8;   //Read the upper byte
  
      //Store data from the specific channel
      //Halt acquisition after 'tam' samples and start transmission
  if (sendStatus == false){
    CH = ADMUX & 0x0F;
    dataVector[CH][counter] = sample;   //Store the data
          //Verify if all channels were acquired
    if (++CH < N)
      ADMUX += 1;    //If not, go to the next channel
    else{
      ADMUX &= 0xF0; //If so, turn to channel 0 and
      counter++;     //update the number of samples
    }
    
      //Verify if it is time to transmit
    if (counter == tam){
      counter = 0;
      sendStatus = true;
    }  
  }
}


//-----------------------------
//TIMER interrupt service routine
ISR(TIMER0_COMPA_vect) {
    /* just clears the flag, as needed, but can be used for secondary ADC actions */
    /* In this example just toggles the digital output 7 at timer_clk/2 Hz */
  static bool toogle = true;
  static int counter = 0;

  if (counter == 60){
    counter = 0;    
    if (toogle) {
      //digitalWrite(LED_BUILTIN, HIGH);
      digitalWrite(7, HIGH);
      toogle = false;
    } else {
      //digitalWrite(LED_BUILTIN, LOW);
      digitalWrite(7, LOW);
      toogle = true;
    }
  }
  else
    counter++;
}


//--------------------------------------
//Loop to send data to the main computer
void loop()
{
  int i,j;
  char cmd;
  float voltage=0.0f;
  float current=0.0f;
  float lux=0.0f;
  float temp=0.0f;
  float signalValues=0.0f;
    //Verify if it is time to transmit data
  if (sendStatus == true){
      //Wait for the command from the host
    /*cmd = 'x';
    while (1){
      if (Serial.available() > 0)
        cmd = Serial.read();
    }*/
      //Transmit the data
    for(i=0; i<tam; i++){   
      for(j=0; j<(N-1); j++){
        //Serial.print(dataVector[j][i]);
        //Serial.print("\t");
        signalValues = float(dataVector[j][i]);
        switch(j)
        {
          case 1:
            voltage = signalValues;
            break;
          case 2:
            lux = signalValues;
            break;
          case 3:
            current = signalValues;
            break;
          case 4:
            temp = signalValues;
            break;
        }
      }
      signalValues =dataVector[N-1][i];
      //Serial.println(signalValues);
      Serial.println(dataVector[0][i]);
    }
      //Restart acquisition
    noInterrupts();
    sendStatus = false;
    interrupts();
  }
}