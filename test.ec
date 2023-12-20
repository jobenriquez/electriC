Main
{
  `
  float timeInMinutes = 3.5;
  float timeInSeconds = 0; //This is a comment
  float amperes = 20.0; 
  /* This is 
    also a 
    comment */
  float charge = 0;
  timeInSeconds = MTS(timeInMinutes); //Comment 3
  charge = CCH(timeInSeconds);
  PrintLine(charge); 
  message = "hello world"
}

    
