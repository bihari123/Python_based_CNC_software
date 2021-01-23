#include <AccelStepper.h>
#include <Servo.h>                                                              // Add library

Servo my_servo;  

int servo_position = 0 ;

                                                                                            // Motor shield has two motor ports,
                                                                                            //  now we'll wrap them in 
                                                                                            //  an AccelStepper object
AccelStepper stepper1(forwardstep1, backwardstep1);
AccelStepper stepper2(forwardstep2, backwardstep2);
int convertToInt( char a){
  switch (a){
    case '0': return 0;
              break;
    case '1': return 1;
              break;
    case '2': return 2;
              break;
    case '3': return 3;
              break;
    case '4': return 4;
              break;
    case '5': return 5;
              break;
    case '6': return 6;
              break;
    case '7': return 7;
              break;
    case '8': return 8;
              break;
    case '9': return 9;
              break;
     
  }
  
}

void setup()
{   Serial.begin(9600);                                                                              // setting the baud rate
    Serial.println("hello");

    my_servo.attach (10);
    
    stepper1.setMaxSpeed(300.0);
    stepper1.setAcceleration(100.0);
    stepper1.moveTo(0);
    stepper2.setMaxSpeed(300.0);
    stepper2.setAcceleration(100.0);
    stepper2.moveTo(0);
   
   }

void loop() {

    if (Serial.available() > 0) {                                         // checking for serial communication
       
        String serialListener=Serial.readString();             // read the command from the software
        int current_position= my_servo.read();                // read the current position of z axis
        
                                                                                      //up or down servo motor
        if(serialListener[0] == 'U'){                                 // pen is lifted
         my_servo.attach (10);
            for (servo_position =current_position; servo_position <=current_position + 90; servo_position +=1){
         
                my_servo.write(servo_position);
                delay(10);
             }  
            my_servo.detach(); 
             
         }
         else if (serialListener[0] == 'D'){                             // pen is dropped
            my_servo.attach (10);
      
             for (servo_position=current_position; servo_position >= current_position - 90; servo_position -=1){
 
                 my_servo.write(servo_position);
                 delay(10);
    
             } 
             my_servo.detach();
         }
  
        
        if (serialListener[0] == 'Y') {                                     // check the axis to move
          if (serialListener[1] == 'N') {                                  // check the direction of movement
                                                                                           //along  the axis
                                                                                          
                                                                                                                                                                                 
                int a=convertToInt(serialListener[2]) ;               // convert the number of steps
                                                                                            // from the command into integer
            a=10*a;
            Serial.print(" a is ");
            Serial.print(a);
            int b=convertToInt(serialListener[3]);
            Serial.print(" b is ");
            Serial.print(b);
            int increment = 12*(a+b);                                                       // multiply with minimum 
                                                                                                                         //resolution factor
            stepper1.moveTo(stepper1.currentPosition()-increment);                    // move the axis
           
          }
          else if (serialListener[1] == 'P') {
            int a=convertToInt(serialListener[2]);
            a=10*a;
            Serial.print(" a is ");
            Serial.print(a);
            int b=convertToInt(serialListener[3]);
            Serial.print(" b is ");
            Serial.print(b);
            int increment = 12*(a+b);
            stepper1.moveTo(stepper1.currentPosition()+increment);
          }
         }
         else if (serialListener[0] == 'X') {
            if (serialListener[1] == 'P') {
            int a=convertToInt(serialListener[2]);
            a=10*a;
            Serial.print(" a is ");
            Serial.print(a);
            int b=convertToInt(serialListener[3]);
            Serial.print(" b is ");
            Serial.print(b);
            int increment = 12*(a+b);
            stepper2.moveTo(stepper2.currentPosition()-increment);
            //stepper2.moveTo(0);  
              
            }
            else if (serialListener[1] == 'N') {
            int a=convertToInt(serialListener[2]);
            a=10*a;
            Serial.print(" a is ");
            Serial.print(a);
            int b=convertToInt(serialListener[3]);
            Serial.print(" b is ");
            Serial.print(b);
            int increment = 12*(a+b);
            stepper2.moveTo(stepper2.currentPosition()+increment);
            //stepper2.moveTo(0);
              
            }
        }
                                                                                                    // for diagonal Movement
        else if (serialListener[0] == 'T') {
          if (serialListener[1] == 'X' && serialListener[2] == 'N' && serialListener[3] == 'Y' && serialListener[4] == 'N'){
            int a=convertToInt(serialListener[5]);
            a=10*a;
            Serial.print(" a is ");
            Serial.print(a);
            int b=convertToInt(serialListener[6]);
            Serial.print(" b is ");
            Serial.print(b);
            int increment = 12*(a+b);
            stepper1.moveTo(stepper1.currentPosition()- increment);
            stepper2.moveTo(stepper2.currentPosition()+increment);
          }
          else if  (serialListener[1] == 'X' && serialListener[2] == 'N' && serialListener[3] == 'Y' && serialListener[4] == 'P'){
            int a=convertToInt(serialListener[5]);
            a=10*a;
            Serial.print(" a is ");
            Serial.print(a);
            int b=convertToInt(serialListener[6]);
            Serial.print(" b is ");
            Serial.print(b);
            int increment = 12*(a+b);
            stepper1.moveTo(stepper1.currentPosition()+ increment);
            stepper2.moveTo(stepper2.currentPosition()+increment);
          }
          else if  (serialListener[1] == 'X' && serialListener[2] == 'P' && serialListener[3] == 'Y' && serialListener[4] == 'N'){
            int a=convertToInt(serialListener[5]);
            a=10*a;
            Serial.print(" a is ");
            Serial.print(a);
            int b=convertToInt(serialListener[6]);
            Serial.print(" b is ");
            Serial.print(b);
            int increment = 12*(a+b);
            stepper1.moveTo(stepper1.currentPosition()- increment);
            stepper2.moveTo(stepper2.currentPosition()-increment);
          }
          else if  (serialListener[1] == 'X' && serialListener[2] == 'P' && serialListener[3] == 'Y' && serialListener[4] == 'P'){
            int a=convertToInt(serialListener[5]);
            a=10*a;
            Serial.print(" a is ");
            Serial.print(a);
            int b=convertToInt(serialListener[6]);
            Serial.print(" b is ");
            Serial.print(b);
            int increment = 12*(a+b);
            stepper1.moveTo(stepper1.currentPosition()+ increment);
            stepper2.moveTo(stepper2.currentPosition()-increment);
          }
        }   
           
    }
    stepper2.run();  
    stepper1.run();
}
