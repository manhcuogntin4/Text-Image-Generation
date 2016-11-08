#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <sstream>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <iostream>
#include <fstream>
using namespace cv; 
using namespace std;

int main(int argc, char* argv[])
{
    char *outText;

    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    // Initialize tesseract-ocr with English, without specifying tessdata path
    if (api->Init(NULL, "fra")) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    // Open input image with leptonica library
    //Pix *image = pixRead(argv[1]);
    std::string input_path = argv[1];
    //cv::Mat im = cv::imread(input_path, 0);
  Size size(700,50);
   Mat src=imread(input_path,0);
  imshow("Origin",src);
 waitKey(0);
  std::string label="Hello World";
  
     string line;
  ifstream myfile (argv[2]);
  if (myfile.is_open())
  {
    while ( getline (myfile,line) )
    {
	Mat tmp;      
	resize(src,tmp,size);	
	cout << line << '\n';
	putText(tmp, line, Point(10, tmp.rows*3/4 ), FONT_HERSHEY_PLAIN, 3.0, CV_RGB(0,255,0), 	2.0);
        //imshow(line,tmp);
	imwrite(line+".bin.png", tmp);
	//waitKey(0);
	ofstream myfile(line+".gt.txt");
	if (myfile.is_open())
  	{
	myfile<<line;
	myfile.close();
	}
    }
    myfile.close();
  }
  //putText(src, label, Point(10, src.rows*3/4 ), FONT_HERSHEY_PLAIN, 3.0, CV_RGB(0,255,0), 2.0);
  //imshow("Text",src);
 

    return 0;
}


