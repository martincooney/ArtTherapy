
//run this, the python backend, soundplay, and speech recognition

//INCLUDES

#include "ros/ros.h"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>  
#include "std_msgs/String.h"

//DEFINES

#define total_width 400 
#define total_length 600
#define buttonLength 200

//NAMESPACES

using namespace std;
using namespace cv;

//FUNCTION DECLARATIONS

void drawStuff();
void mouseCallBackFunc(int event, int x, int y, int flags, void* userdata);

//GLOBAL VARS

char aWin[] = "Baxter Simple Art Therapy Demo";
Mat image;
int text_offset_x=10, text_offset_y=20+20;
int col1_x=30;
int offset_y = 20;

//CLASSES

class rosStuff{
  public:
  ros::NodeHandle n;
  ros::Publisher top_pub; 
};



// MAIN FUNCTION


int main(int argc, char **argv){
  
  ros::init(argc, argv, "baxter_simple_demo");

  ROS_INFO("--------------------------------------");
  ROS_INFO("-   Baxter simple art therapy demo   -");
  ROS_INFO("-   for art and teaching (C++)       -");
  ROS_INFO("-   DEC 2016, HH, Martin             -");
  ROS_INFO("--------------------------------------");

  ros::Time::init();
  ros::Rate loop_rate(10);
  rosStuff stuff;
  stuff.top_pub= stuff.n.advertise<std_msgs::String>("to_baxter", 1000);

  namedWindow(aWin, 1);
  setMouseCallback(aWin, mouseCallBackFunc, &stuff); 
  moveWindow(aWin, 100, 0);
  drawStuff();

  //wait a little bit to let ROS get started
  loop_rate.sleep();
  loop_rate.sleep();
  loop_rate.sleep();	      
  ros::spinOnce();
  loop_rate.sleep();

  int keyPressed=0;
  while(keyPressed!=27 && ros::ok()){ //27 is the escape key
    ros::spinOnce();
    loop_rate.sleep();
    keyPressed= waitKey(10); 
  }

  return 0;
}


void drawStuff(){
  
  image = Mat::zeros(total_length, total_width, CV_8UC3 );

  //draw buttons   
  rectangle(image, Point(col1_x, offset_y+10), Point(col1_x+buttonLength, offset_y+40), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+50), Point(col1_x+buttonLength, offset_y+80), Scalar(255, 255, 255), -1, 8); 
  rectangle(image, Point(col1_x, offset_y+90), Point(col1_x+buttonLength, offset_y+120), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+130), Point(col1_x+buttonLength, offset_y+160), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+170), Point(col1_x+buttonLength, offset_y+200), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+210), Point(col1_x+buttonLength, offset_y+240), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+250), Point(col1_x+buttonLength, offset_y+280), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+290), Point(col1_x+buttonLength, offset_y+320), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+330), Point(col1_x+buttonLength, offset_y+360), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+370), Point(col1_x+buttonLength, offset_y+400), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+410), Point(col1_x+buttonLength, offset_y+440), Scalar(255, 255, 255), -1, 8);
  rectangle(image, Point(col1_x, offset_y+450), Point(col1_x+buttonLength, offset_y+480), Scalar(255, 255, 255), -1, 8);

  //draw labels
  putText(image, "Commands", Point(col1_x+text_offset_x, 10+10), 1, 1.0, Scalar(255, 255, 255), 1, 8);
  putText(image, "0", Point(col1_x+text_offset_x, 10+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "1", Point(col1_x+text_offset_x, 50+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "2", Point(col1_x+text_offset_x, 90+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "3", Point(col1_x+text_offset_x, 130+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "4", Point(col1_x+text_offset_x, 170+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "5", Point(col1_x+text_offset_x, 210+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "6 Art Therapy", Point(col1_x+text_offset_x, 250+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "7", Point(col1_x+text_offset_x, 290+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "8", Point(col1_x+text_offset_x, 330+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "9", Point(col1_x+text_offset_x, 370+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "10", Point(col1_x+text_offset_x, 410+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);
  putText(image, "11", Point(col1_x+text_offset_x, 450+text_offset_y), 1, 1.0, Scalar(0, 0, 0), 1, 8);

  imshow(aWin, image);
}


//this is set up to be flexible so buttons can have any desired functionality
void mouseCallBackFunc(int event, int x, int y, int flags, void* userdata){  
  
  rosStuff* r=(rosStuff*)userdata;
  time_t t = time(0);  
  
  if(event == EVENT_LBUTTONDOWN){
    cout << x << ", " << y << endl;

    if((x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+10) && (y<offset_y+40)){
      	ROS_INFO("00");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "00"; 
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if((x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+50) && (y<offset_y+80)){
      	ROS_INFO("01");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "01";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if((x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+90) && (y<offset_y+120)){
      	ROS_INFO("02");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "02";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if( (x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+130) && (y<offset_y+160)){
      	ROS_INFO("03");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "03";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if((x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+170) && (y<offset_y+200)){
      	ROS_INFO("04");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "04";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if( (x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+210) && (y<offset_y+240)){
      	ROS_INFO("05");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "05";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if((x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+250) && (y<offset_y+280)){
      	ROS_INFO("06");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "06";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if( (x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+290) && (y<offset_y+320)){
 
     	ROS_INFO("07");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "07";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if((x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+330) && (y<offset_y+360)){

      	ROS_INFO("08");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "08";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    	
    }
    else if((x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+370) && (y<offset_y+400)){
      	ROS_INFO("09");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "09";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if((x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+410) && (y<offset_y+440)){
      	ROS_INFO("10");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "10";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }
    else if((x > col1_x) && (x < col1_x+buttonLength) && (y>offset_y+450) && (y<offset_y+480)){
      	ROS_INFO("11");
  	ros::Rate loop_rate(10);

        std_msgs::String msg;
        std::stringstream ss;
        ss << "11";
        msg.data = ss.str();
        r->top_pub.publish(msg);

    	ros::spinOnce();
    	loop_rate.sleep();
    }

  }
  
  drawStuff();
}






