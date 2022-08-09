#include <ax12.h>
#include <BioloidController.h>

void setup()
{
  //Set motor to wheel mode
  ax12SetRegister2(3, AX_CCW_ANGLE_LIMIT_L, 0); //inner
  ax12SetRegister2(2, AX_CCW_ANGLE_LIMIT_L, 0); //outer
  delay(1000);
}

void loop()
{
  ax12SetRegister2(2, AX_GOAL_SPEED_L, 50); //inner
  ax12SetRegister2(3, AX_GOAL_SPEED_L, 4); //outer
  Serial.println(inner);
  delay(250);
}
