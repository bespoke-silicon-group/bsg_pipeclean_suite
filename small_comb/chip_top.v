module chip_top 
  ( input   [7:0] a_i
  , input   [7:0] b_i
  , output [15:0] c_o
  );

  assign c_o = a_i * b_i;

endmodule

