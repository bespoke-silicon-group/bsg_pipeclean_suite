module hard_mem_1rw_bit_mask_d64_w15_wrapper #( parameter width_p = 15
					                                    , parameter els_p   = 64
					                                    , parameter addr_width_lp = $clog2(els_p)
                                              )
  ( input                      clk_i
  , input                      reset_i
  , input [width_p-1:0]        data_i
  , input [addr_width_lp-1:0]  addr_i
  , input                      v_i
  , input [width_p-1:0]        w_mask_i
  , input                      w_i
  , output wire [width_p-1:0]  data_o
  );

// synopsys translate_off

  // This should only be defined during RTL simulations. During synthesis items
  // between these tags are not evaluated thus this will remain undefined.
  `define BSG_NOT_SYNTHESIS

// synopsys translate_on

`ifndef BSG_NOT_SYNTHESIS

  // TODO: Add the instantiation of the hardened module with proper pin
  // mapping. Use the RTL sytnesizable model below and verify it matches the
  // semantics of the hardened block. You may add logic to make the semantics
  // match if needed.

  //hard_mem_1rw_bit_mask_d64_w15
  //  mem
  //    ( ...
  //    );

`else

  // Synthesizable RTL model. Use this for siumulations and to make sure that
  // the semantics of the hardened block matches that of the RTL as semantics
  // of various hardened blocks can change between processes.

  wire unused = reset_i;

  reg [addr_width_lp-1:0] addr_r;
  reg [els_p-1:0][width_p-1:0] mem;

  genvar i;

  always @(posedge clk_i)
    if (v_i)
      begin
         if (w_i)
           begin
             for (i = 0; i < width_p; i=i+1)
               if (w_mask_i[i])
                 mem[addr_i][i] <= data_i[i];
           end
         else
           begin
             addr_r <= addr_i;
           end
      end

  assign data_o = mem[addr_r];

`endif

endmodule

