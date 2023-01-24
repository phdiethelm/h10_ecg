#pragma endian little
#pragma pattern_limit 16777216


#include <std/sys.pat>
#include <std/mem.pat>
#include <std/math.pat>
#include <type/time.pat>

enum Frame_types_ECG : u8 {
    Electrocardiogram = 0,
};

enum PMD_Measurement_Types : u8 {
    ECG = 0,
    PPG = 1,
    Acceleration = 2,
    PP_Interval = 3,
    Gyroscope = 5,
    Magnetometer = 6,
};

struct StreamDataFromDevice {
    if($+4 <= std::mem::size()) {
        u32                     length;
        
        if ($+length <= std::mem::size()) {
            PMD_Measurement_Types   type;
            u64                     last_sample_timestamp_in_ns;
            
            if(type == PMD_Measurement_Types::ECG) {
                Frame_types_ECG     frame_type;
                s24                 samples[(length - 10) / 3];
            } else {
                u8                  frame_type;
                u8                  data[length-10];
            }
        }
    }
};


struct StreamFile {
    char magic[24];
    StreamDataFromDevice data[while($ < std::mem::size())];
//    StreamDataFromDevice data[2];
    
    std::assert(magic == "H10 ECG v1.0 binary data", "Invalid magic value!");
};

StreamFile streamfile @ 0;

