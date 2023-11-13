#include <opencv2/opencv.hpp>
#include <iostream>
#include <compress.hpp>

int main(){
	std::chrono::high_resolution_clock timer;
	cv::Mat frame;
	std::string payload;
	std::vector<uint8_t> jpegBuffer;
	std::vector<int> params;
	params.push_back(cv::IMWRITE_JPEG_QUALITY);
	params.push_back(80); 
	cv::VideoCapture cap( 0 ); 
	for(;;){
		auto start = timer.now();
		cap >> frame;
		cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
		cv::imencode(".jpg", frame, jpegBuffer, params);
		payload = gzip::compress(reinterpret_cast<const char*>(jpegBuffer.data()), jpegBuffer.size());
		auto stop = timer.now();
		auto deltaTime = std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count() / 1000.0f;
		std::cout << deltaTime << "\n";
		
	}
	cap.release();
}
