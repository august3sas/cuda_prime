# Makefile for compiling and running a CUDA program

# Compiler
NVCC := nvcc

# Target executable
TARGET := primes

# Source files
SRCS := primes.cu

# Determine the architecture
ARCH := sm_61  # Update this to the correct architecture for your GPU

# Compiler flags
NVCC_FLAGS := -arch=$(ARCH)

# Default rule
all: $(TARGET)

# Rule to build the executable
$(TARGET): $(SRCS)
	$(NVCC) $(NVCC_FLAGS) -o $@ $^

# Rule to clean up the directory
clean:
	rm -f $(TARGET)

# Rule to run the program
run: $(TARGET)
	./$(TARGET)
