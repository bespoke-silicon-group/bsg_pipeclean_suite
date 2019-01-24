module chip_top 
  ( input  [31:0] a_i
  , input  [31:0] b_i
  , output [63:0] c_o
  );

  assign c_o = a_i * b_i;

endmodule

