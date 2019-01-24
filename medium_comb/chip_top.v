module multiplier #(parameter width_p="inv")
  ( input      [width_p-1:0] a_i
  , input      [width_p-1:0] b_i
  , output [(2*width_p)-1:0] c_o
  );

  assign c_o = a_i * b_i;

endmodule

module chip_top
  ( input  [31:0] a_i
  , input  [31:0] b_i
  , output [63:0] c_o
  );

  multiplier #(.width_p(32)) MULT
    (.a_i(a_i)
    ,.b_i(b_i)
    ,.c_o(c_o)
    );

endmodule

