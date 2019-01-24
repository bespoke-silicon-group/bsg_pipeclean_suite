# In-order to use this constraint file, you will need to set an environment
# variable called FO4 that is equal to the fan-out-of-4 value for the process.

# Create a virtual clock to constrain the pure-combinational design
create_clock -name vclk -period [expr 70 * $env(FO4)]
set_input_delay  0 -clock vclk [all_inputs]
set_output_delay 0 -clock vclk [all_outputs]

