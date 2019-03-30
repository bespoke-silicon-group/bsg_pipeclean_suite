////////////////////////////////////////////////////////////////////////////////////////////////////

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

  // TODO: Replace the sythesizable RTL model below with the hardened
  // equivilant. Use the RTL model to check the sematics of the harden block
  // match.
  //
  // NOTE: The instance name of the hardened block is expected to be "mem".

  //hard_mem_1rw_bit_mask_d64_w15
  //  mem
  //    ( ...
  //    );

  // BEGIN SYNTHESIZABLE RTL MODEL

  // synopsys translate_off
  initial
    begin
      $display("## %m: to get the expect quality of results, this module should be replaced with the hardened equivalent.");
    end
  // synopsys translate_on

  wire unused = reset_i;
  reg [addr_width_lp-1:0] addr_r;
  reg [els_p-1:0][width_p-1:0] mem;
  int i;
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

  // END SYNTHESIZABLE RTL MODEL

endmodule

////////////////////////////////////////////////////////////////////////////////////////////////////

module hard_mem_1rw_bit_mask_d64_w7_wrapper #( parameter width_p = 7
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

  // TODO: Replace the sythesizable RTL model below with the hardened
  // equivilant. Use the RTL model to check the sematics of the harden block
  // match.
  //
  // NOTE: The instance name of the hardened block is expected to be "mem".

  //hard_mem_1rw_bit_mask_d64_w7
  //  mem
  //    ( ...
  //    );

  // BEGIN SYNTHESIZABLE RTL MODEL

  // synopsys translate_off
  initial
    begin
      $display("## %m: to get the expect quality of results, this module should be replaced with the hardened equivalent.");
    end
  // synopsys translate_on

  wire unused = reset_i;
  reg [addr_width_lp-1:0] addr_r;
  reg [width_p-1:0] mem [els_p-1:0];
  int i;
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

  // END SYNTHESIZABLE RTL MODEL

endmodule

////////////////////////////////////////////////////////////////////////////////////////////////////

module hard_mem_1rw_bit_mask_d64_w96_wrapper #( parameter width_p = 96
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

  // TODO: Replace the sythesizable RTL model below with the hardened
  // equivilant. Use the RTL model to check the sematics of the harden block
  // match.
  //
  // NOTE: The instance name of the hardened block is expected to be "mem".

  //hard_mem_1rw_bit_mask_d64_w96
  //  mem
  //    ( ...
  //    );

  // BEGIN SYNTHESIZABLE RTL MODEL

  // synopsys translate_off
  initial
    begin
      $display("## %m: to get the expect quality of results, this module should be replaced with the hardened equivalent.");
    end
  // synopsys translate_on

  wire unused = reset_i;
  reg [addr_width_lp-1:0] addr_r;
  reg [els_p-1:0][width_p-1:0] mem;
  int i;
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

  // END SYNTHESIZABLE RTL MODEL

endmodule

////////////////////////////////////////////////////////////////////////////////////////////////////

module hard_mem_1rw_byte_mask_d512_w64_wrapper #( parameter width_p = 64
                                                , parameter els_p = 512
                                                , parameter addr_width_lp = $clog2(els_p)
                                                , parameter write_mask_width_lp = width_p>>3
                                                )
  ( input                            clk_i
  , input                            reset_i
  , input [width_p-1:0]              data_i
  , input [addr_width_lp-1:0]        addr_i
  , input                            v_i
  , input [write_mask_width_lp-1:0]  write_mask_i
  , input                            w_i
  , output wire [width_p-1:0]        data_o
  );

  // TODO: Replace the sythesizable RTL model below with the hardened
  // equivilant. Use the RTL model to check the sematics of the harden block
  // match.
  //
  // NOTE: The instance name of the hardened block is expected to be "mem".

  //hard_mem_1rw_byte_mask_d512_w64
  //  mem
  //    ( ...
  //    );

  // BEGIN SYNTHESIZABLE RTL MODEL

  // synopsys translate_off
  initial
    begin
      $display("## %m: to get the expect quality of results, this module should be replaced with the hardened equivalent.");
    end
  // synopsys translate_on

  wire unused = reset_i;
  reg [addr_width_lp-1:0] addr_r;
  reg [width_p-1:0] mem [els_p-1:0];
  int i;
  always @(posedge clk_i)
    if (v_i)
      begin
        if (w_i)
          begin
            for (i = 0; i < write_mask_width_lp; i=i+1)
              if (write_mask_i[i])
                mem[addr_i][(i*8)+:8] <= data_i[(i*8)+:8];
          end
        else
          begin
            addr_r <= addr_i;
          end
      end
  assign data_o = mem[addr_r];

  // END SYNTHESIZABLE RTL MODEL
  
endmodule

////////////////////////////////////////////////////////////////////////////////////////////////////

module hard_mem_1rw_d256_w95_wrapper #( parameter width_p = 95
                                      , parameter els_p = 256
                                      , parameter addr_width_lp = $clog2(els_p)
                                      )
  ( input                     clk_i
  , input                     v_i
  , input                     reset_i
  , input [width_p-1:0]       data_i
  , input [addr_width_lp-1:0] addr_i
  , input                     w_i
  , output wire [width_p-1:0] data_o
  );

  // TODO: Replace the sythesizable RTL model below with the hardened
  // equivilant. Use the RTL model to check the sematics of the harden block
  // match.
  //
  // NOTE: The instance name of the hardened block is expected to be "mem".

  //hard_mem_1rw_d256_w95
  //  mem
  //    ( ...
  //    );

  // BEGIN SYNTHESIZABLE RTL MODEL

  // synopsys translate_off
  initial
    begin
      $display("## %m: to get the expect quality of results, this module should be replaced with the hardened equivalent.");
    end
  // synopsys translate_on

  wire unused = reset_i;
  reg [addr_width_lp-1:0] addr_r;
  reg [width_p-1:0] mem [els_p-1:0];
  always @(posedge clk_i)
    if (v_i)
      begin
        if (w_i)
          mem[addr_i] <= data_i;
        else
          addr_r <= addr_i;
      end
  assign data_o = mem[addr_r];

  // END SYNTHESIZABLE RTL MODEL

endmodule

////////////////////////////////////////////////////////////////////////////////////////////////////

module hard_mem_1rw_d512_w64_wrapper #( parameter width_p = 64
                                      , parameter els_p = 512
                                      , parameter addr_width_lp = $clog2(els_p)
                                      )
  ( input                     clk_i
  , input                     v_i
  , input                     reset_i
  , input [width_p-1:0]       data_i
  , input [addr_width_lp-1:0] addr_i
  , input                     w_i
  , output wire [width_p-1:0] data_o
  );

  // TODO: Replace the sythesizable RTL model below with the hardened
  // equivilant. Use the RTL model to check the sematics of the harden block
  // match.
  //
  // NOTE: The instance name of the hardened block is expected to be "mem".

  //hard_mem_1rw_d512_w64
  //  mem
  //    ( ...
  //    );

  // BEGIN SYNTHESIZABLE RTL MODEL

  // synopsys translate_off
  initial
    begin
      $display("## %m: to get the expect quality of results, this module should be replaced with the hardened equivalent.");
    end
  // synopsys translate_on

  wire unused = reset_i;
  reg [addr_width_lp-1:0] addr_r;
  reg [width_p-1:0] mem [els_p-1:0];
  always @(posedge clk_i)
    if (v_i)
      begin
        if (w_i)
          mem[addr_i] <= data_i;
        else
          addr_r <= addr_i;
      end
  assign data_o = mem[addr_r];

  // END SYNTHESIZABLE RTL MODEL

endmodule

////////////////////////////////////////////////////////////////////////////////////////////////////

