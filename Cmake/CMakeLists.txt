cmake_minimum_required(VERSION 3.10)
project(video_player C)

set(CMAKE_C_STANDARD 11)

# Define library locations based on your folders
set(FFMPEG_DIR "C:/ffmpeg/ffmpeg-master-latest-win64-gpl-shared")
set(SDL3_DIR "C:/SDL3/x86_64-w64-mingw32")

# Include Headers
include_directories(
        "${FFMPEG_DIR}/include"
        "${SDL3_DIR}/include"
)

# Link Libraries
link_directories(
        "${FFMPEG_DIR}/lib"
        "${SDL3_DIR}/lib"
)

add_library(video_player SHARED main.c)
#add_executable(audio_player audio.c)

# Link the required binaries
# Note: SDL3 generally only requires linking against 'SDL3'
target_link_libraries(video_player
        SDL3
        avformat
        avcodec
        avutil
        swscale
        swresample
)
