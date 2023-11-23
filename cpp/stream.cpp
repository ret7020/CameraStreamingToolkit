#include <opencv2/opencv.hpp>
#include <iostream>
#include <compress.hpp>
#include "crow_all.h"

int main()
{
	crow::SimpleApp app;

	std::chrono::high_resolution_clock timer;
	cv::Mat frame;
	std::string payload;
	std::vector<uint8_t> jpegBuffer;
	std::vector<int> params;
	params.push_back(cv::IMWRITE_JPEG_QUALITY);
	params.push_back(80);
	cv::VideoCapture cap(0);
	cap.set(cv::CAP_PROP_FRAME_WIDTH, 640.0);
	cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480.0);

	CROW_ROUTE(app, "/ws")
		.websocket()
		.onopen([&](crow::websocket::connection &conn)
				{
					CROW_LOG_INFO << "new connection";
					for (;;)
					{
						
						cap >> frame;
						cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
						cv::imencode(".jpg", frame, jpegBuffer, params);
						payload = gzip::compress(reinterpret_cast<const char *>(jpegBuffer.data()), jpegBuffer.size());
						conn.send_text(payload);
					} });

	app.port(5000).multithreaded().run();
}
