
SRC_FILES := $(wildcard src/*.cpp)
OBJ_FILES := $(SRC_FILES)
OBJ_FILES := $(notdir $(OBJ_FILES))
OBJ_FILES := $(addprefix obj/, $(OBJ_FILES))
OBJ_FILES := $(OBJ_FILES:%.cpp=%.o)
BIN_FILE := bin/arp

all: folders $(BIN_FILE)

$(BIN_FILE): $(OBJ_FILES)
	g++ -o $@ $(OBJ_FILES) -lpcap

obj/%.o: src/%.cpp
	g++ -o $@ -c $^

folders:
	mkdir -p obj/ bin/

clean:
	rm -rf bin/ obj/
