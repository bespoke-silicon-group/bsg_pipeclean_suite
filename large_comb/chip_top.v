module chip_top 
  ( input  [127:0] a_i
  , input  [127:0] b_i
  , output [255:0] c_o
  );

  assign c_o = a_i * b_i;

endmodule

