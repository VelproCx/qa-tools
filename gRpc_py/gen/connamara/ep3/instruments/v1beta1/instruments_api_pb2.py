# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connamara/ep3/instruments/v1beta1/instruments_api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gen.connamara.ep3.instruments.v1beta1 import instruments_pb2 as connamara_dot_ep3_dot_instruments_dot_v1beta1_dot_instruments__pb2
from gen.connamara.ep3.instruments.v1beta1 import swaps_pb2 as connamara_dot_ep3_dot_instruments_dot_v1beta1_dot_swaps__pb2
from gen.connamara.ep3.instruments.v1beta1 import derivatives_pb2 as connamara_dot_ep3_dot_instruments_dot_v1beta1_dot_derivatives__pb2
from gen.connamara.ep3.instruments.v1beta1 import multileg_pb2 as connamara_dot_ep3_dot_instruments_dot_v1beta1_dot_multileg__pb2
from gen.connamara.ep3.instruments.v1beta1 import event_pb2 as connamara_dot_ep3_dot_instruments_dot_v1beta1_dot_event__pb2
from gen.connamara.ep3.type.v1beta1 import type_pb2 as connamara_dot_ep3_dot_type_dot_v1beta1_dot_type__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7connamara/ep3/instruments/v1beta1/instruments_api.proto\x12!connamara.ep3.instruments.v1beta1\x1a\x33\x63onnamara/ep3/instruments/v1beta1/instruments.proto\x1a-connamara/ep3/instruments/v1beta1/swaps.proto\x1a\x33\x63onnamara/ep3/instruments/v1beta1/derivatives.proto\x1a\x30\x63onnamara/ep3/instruments/v1beta1/multileg.proto\x1a-connamara/ep3/instruments/v1beta1/event.proto\x1a%connamara/ep3/type/v1beta1/type.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x19google/protobuf/any.proto\"\x15\n\x13ListProductsRequest\"T\n\x14ListProductsResponse\x12<\n\x08products\x18\x01 \x03(\x0b\x32*.connamara.ep3.instruments.v1beta1.Product\"S\n\x14\x43reateProductRequest\x12;\n\x07product\x18\x01 \x01(\x0b\x32*.connamara.ep3.instruments.v1beta1.Product\"T\n\x15\x43reateProductResponse\x12;\n\x07product\x18\x01 \x01(\x0b\x32*.connamara.ep3.instruments.v1beta1.Product\"S\n\x14UpdateProductRequest\x12;\n\x07product\x18\x01 \x01(\x0b\x32*.connamara.ep3.instruments.v1beta1.Product\"T\n\x15UpdateProductResponse\x12;\n\x07product\x18\x01 \x01(\x0b\x32*.connamara.ep3.instruments.v1beta1.Product\"\'\n\x11GetProductRequest\x12\x12\n\nproduct_id\x18\x01 \x01(\t\"Q\n\x12GetProductResponse\x12;\n\x07product\x18\x01 \x01(\x0b\x32*.connamara.ep3.instruments.v1beta1.Product\"*\n\x14\x44\x65leteProductRequest\x12\x12\n\nproduct_id\x18\x01 \x01(\t\"\x17\n\x15\x44\x65leteProductResponse\"\x1a\n\x18ListenInstrumentsRequest\"^\n\x19ListenInstrumentsResponse\x12\x41\n\ninstrument\x18\x01 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.Instrument\"\x14\n\x12GetMetadataRequest\"\x9e\x01\n\x13GetMetadataResponse\x12V\n\x08metadata\x18\x01 \x03(\x0b\x32\x44.connamara.ep3.instruments.v1beta1.GetMetadataResponse.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"-\n\x14GetInstrumentRequest\x12\x15\n\rinstrument_id\x18\x01 \x01(\t\"Z\n\x15GetInstrumentResponse\x12\x41\n\ninstrument\x18\x01 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.Instrument\"\\\n\x17\x43reateInstrumentRequest\x12\x41\n\ninstrument\x18\x01 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.Instrument\"]\n\x18\x43reateInstrumentResponse\x12\x41\n\ninstrument\x18\x01 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.Instrument\"0\n\x17\x44\x65leteInstrumentRequest\x12\x15\n\rinstrument_id\x18\x01 \x01(\t\"\x1a\n\x18\x44\x65leteInstrumentResponse\"c\n\x1eUpdatePendingInstrumentRequest\x12\x41\n\ninstrument\x18\x01 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.Instrument\"d\n\x1fUpdatePendingInstrumentResponse\x12\x41\n\ninstrument\x18\x01 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.Instrument\"\xe1\x01\n\x1cUpdateInstrumentStateRequest\x12\x15\n\rinstrument_id\x18\x01 \x01(\t\x12\x14\n\x0cis_scheduled\x18\x02 \x01(\x08\x12\x41\n\x05state\x18\x03 \x01(\x0e\x32\x32.connamara.ep3.instruments.v1beta1.InstrumentState\x12\x14\n\x0cnon_blocking\x18\x04 \x01(\x08\x12;\n\x17schedule_execution_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"b\n\x1dUpdateInstrumentStateResponse\x12\x41\n\ninstrument\x18\x01 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.Instrument\"\xab\x01\n\x1cUpdateInstrumentStatsRequest\x12\x15\n\rinstrument_id\x18\x01 \x01(\t\x12\x41\n\x05stats\x18\x02 \x01(\x0b\x32\x32.connamara.ep3.instruments.v1beta1.InstrumentStats\x12\x31\n\rtransact_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x1f\n\x1dUpdateInstrumentStatsResponse\"\xa2\x01\n\x16UpdateLastPriceRequest\x12\x15\n\rinstrument_id\x18\x01 \x01(\t\x12\x12\n\nlast_price\x18\x02 \x01(\x03\x12\x31\n\rtransact_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x15\n\rlast_quantity\x18\x04 \x01(\x03\x12\x13\n\x0bonly_volume\x18\x05 \x01(\x08\"\x19\n\x17UpdateLastPriceResponse\"\xaa\x01\n\x1cUpdateSettlementPriceRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x18\n\x10settlement_price\x18\x02 \x01(\x03\x12\x31\n\rtransact_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1e\n\x16settlement_preliminary\x18\x04 \x01(\x08\x12\r\n\x05\x63lear\x18\x05 \x01(\x08\"\x1f\n\x1dUpdateSettlementPriceResponse\"\x93\x01\n\x19UpdateOpenInterestRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x15\n\ropen_interest\x18\x02 \x01(\x03\x12\x31\n\rtransact_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05\x63lear\x18\x04 \x01(\x08\x12\r\n\x05\x64\x65lta\x18\x05 \x01(\x08\"\x1c\n\x1aUpdateOpenInterestResponse\"\xe4\x02\n\x16ListInstrumentsRequest\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12\x12\n\npage_token\x18\x02 \x01(\t\x12\x12\n\nproduct_id\x18\x03 \x01(\t\x12\x13\n\x0bonly_active\x18\x04 \x01(\x08\x12\x0f\n\x07symbols\x18\x05 \x03(\t\x12\x14\n\x0cshow_deleted\x18\x06 \x01(\x08\x12\x42\n\x06states\x18\x07 \x03(\x0e\x32\x32.connamara.ep3.instruments.v1beta1.InstrumentState\x12?\n\x04type\x18\x08 \x01(\x0e\x32\x31.connamara.ep3.instruments.v1beta1.InstrumentType\x12N\n\x0c\x66ilter_state\x18\t \x01(\x0e\x32\x38.connamara.ep3.instruments.v1beta1.SchedulingFilterState\"\x83\x01\n\x17ListInstrumentsResponse\x12\x42\n\x0binstruments\x18\x01 \x03(\x0b\x32-.connamara.ep3.instruments.v1beta1.Instrument\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x0b\n\x03\x65of\x18\x03 \x01(\x08\"\x14\n\x12ListSymbolsRequest\"&\n\x13ListSymbolsResponse\x12\x0f\n\x07symbols\x18\x01 \x03(\t\"\xe6\x1d\n\x1dUpdateActiveInstrumentRequest\x12\x15\n\rinstrument_id\x18\x01 \x01(\t\x12i\n\x0cupdate_hours\x18\x02 \x01(\x0b\x32S.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateHoursRequest\x12i\n\x0cupdate_dates\x18\x03 \x01(\x0b\x32S.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateDatesRequest\x12t\n\x12update_price_limit\x18\x04 \x01(\x0b\x32X.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdatePriceLimitRequest\x12}\n\x17update_order_size_limit\x18\x05 \x01(\x0b\x32\\.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateOrderSizeLimitRequest\x12}\n\x17update_hide_market_data\x18\x06 \x01(\x0b\x32\\.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateHideMarketDataRequest\x12x\n\x14update_reject_quotes\x18\x07 \x01(\x0b\x32Z.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateRejectQuotesRequest\x12\x80\x01\n\x18update_holiday_calendars\x18\x08 \x01(\x0b\x32^.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateHolidayCalendarsRequest\x12m\n\x0eupdate_product\x18\t \x01(\x0b\x32U.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateProductRequest\x12o\n\x0fupdate_metadata\x18\n \x01(\x0b\x32V.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateMetadataRequest\x12z\n\x15update_position_limit\x18\x0b \x01(\x0b\x32[.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdatePositionLimitRequest\x12|\n\x16update_type_attributes\x18\x0c \x01(\x0b\x32\\.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateTypeAttributesRequest\x1a_\n\x12UpdateHoursRequest\x12I\n\x10trading_schedule\x18\x01 \x03(\x0b\x32/.connamara.ep3.instruments.v1beta1.TradingHours\x1a\xb8\x04\n\x12UpdateDatesRequest\x12\x34\n\nstart_date\x18\x01 \x01(\x0b\x32 .connamara.ep3.type.v1beta1.Date\x12\x39\n\x0f\x65xpiration_date\x18\x02 \x01(\x0b\x32 .connamara.ep3.type.v1beta1.Date\x12:\n\x10termination_date\x18\x03 \x01(\x0b\x32 .connamara.ep3.type.v1beta1.Date\x12\x19\n\x11start_date_update\x18\x04 \x01(\x08\x12\x1e\n\x16\x65xpiration_date_update\x18\x05 \x01(\x08\x12\x1f\n\x17termination_date_update\x18\x06 \x01(\x08\x12>\n\x0f\x65xpiration_time\x18\x07 \x01(\x0b\x32%.connamara.ep3.type.v1beta1.TimeOfDay\x12\x1e\n\x16\x65xpiration_time_update\x18\x08 \x01(\x08\x12\x39\n\x0flast_trade_date\x18\t \x01(\x0b\x32 .connamara.ep3.type.v1beta1.Date\x12>\n\x0flast_trade_time\x18\n \x01(\x0b\x32%.connamara.ep3.type.v1beta1.TimeOfDay\x12\x1e\n\x16last_trade_date_update\x18\x0b \x01(\x08\x12\x1e\n\x16last_trade_time_update\x18\x0c \x01(\x08\x1a]\n\x17UpdatePriceLimitRequest\x12\x42\n\x0bprice_limit\x18\x01 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.PriceLimit\x1aj\n\x1bUpdateOrderSizeLimitRequest\x12K\n\x10order_size_limit\x18\x01 \x01(\x0b\x32\x31.connamara.ep3.instruments.v1beta1.OrderSizeLimit\x1a\x37\n\x1bUpdateHideMarketDataRequest\x12\x18\n\x10hide_market_data\x18\x01 \x01(\x08\x1a\x32\n\x19UpdateRejectQuotesRequest\x12\x15\n\rreject_quotes\x18\x01 \x01(\x08\x1a:\n\x1dUpdateHolidayCalendarsRequest\x12\x19\n\x11holiday_calendars\x18\x01 \x03(\t\x1a\"\n\x14UpdateProductRequest\x12\n\n\x02id\x18\x01 \x01(\t\x1a\xc0\x01\n\x15UpdateMetadataRequest\x12v\n\x08metadata\x18\x01 \x03(\x0b\x32\x64.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest.UpdateMetadataRequest.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x34\n\x1aUpdatePositionLimitRequest\x12\x16\n\x0eposition_limit\x18\x01 \x01(\x03\x1a\xdf\x08\n\x1bUpdateTypeAttributesRequest\x12\x66\n\x1dinterest_rate_swap_attributes\x18\x01 \x01(\x0b\x32=.connamara.ep3.instruments.v1beta1.InterestRateSwapAttributesH\x00\x12\x31\n\x11\x63ustom_attributes\x18\x02 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x12w\n&forward_rate_agreement_swap_attributes\x18\x03 \x01(\x0b\x32\x45.connamara.ep3.instruments.v1beta1.ForwardRateAgreementSwapAttributesH\x00\x12\x19\n\x0fjson_attributes\x18\x04 \x01(\tH\x00\x12P\n\x11\x66uture_attributes\x18\x05 \x01(\x0b\x32\x33.connamara.ep3.instruments.v1beta1.FutureAttributesH\x00\x12P\n\x11option_attributes\x18\x06 \x01(\x0b\x32\x33.connamara.ep3.instruments.v1beta1.OptionAttributesH\x00\x12T\n\x13multileg_attributes\x18\x07 \x01(\x0b\x32\x35.connamara.ep3.instruments.v1beta1.MultilegAttributesH\x00\x12\x86\x01\n.forward_starting_interest_rate_swap_attributes\x18\x08 \x01(\x0b\x32L.connamara.ep3.instruments.v1beta1.ForwardStartingInterestRateSwapAttributesH\x00\x12W\n\x15\x62\x61sis_swap_attributes\x18\t \x01(\x0b\x32\x36.connamara.ep3.instruments.v1beta1.BasisSwapAttributesH\x00\x12N\n\x10\x65vent_attributes\x18\n \x01(\x0b\x32\x32.connamara.ep3.instruments.v1beta1.EventAttributesH\x00\x12j\n\x1fovernight_index_swap_attributes\x18\x0b \x01(\x0b\x32?.connamara.ep3.instruments.v1beta1.OvernightIndexSwapAttributesH\x00\x12\x66\n\x1dsingle_period_swap_attributes\x18\x0c \x01(\x0b\x32=.connamara.ep3.instruments.v1beta1.SinglePeriodSwapAttributesH\x00\x42\x11\n\x0ftype_attributes\"c\n\x1eUpdateActiveInstrumentResponse\x12\x41\n\ninstrument\x18\x01 \x01(\x0b\x32-.connamara.ep3.instruments.v1beta1.Instrument\"\x1d\n\x1bListHolidayCalendarsRequest\"m\n\x1cListHolidayCalendarsResponse\x12M\n\x11holiday_calendars\x18\x01 \x03(\x0b\x32\x32.connamara.ep3.instruments.v1beta1.HolidayCalendar\"l\n\x1c\x43reateHolidayCalendarRequest\x12L\n\x10holiday_calendar\x18\x01 \x01(\x0b\x32\x32.connamara.ep3.instruments.v1beta1.HolidayCalendar\"m\n\x1d\x43reateHolidayCalendarResponse\x12L\n\x10holiday_calendar\x18\x01 \x01(\x0b\x32\x32.connamara.ep3.instruments.v1beta1.HolidayCalendar\"l\n\x1cUpdateHolidayCalendarRequest\x12L\n\x10holiday_calendar\x18\x01 \x01(\x0b\x32\x32.connamara.ep3.instruments.v1beta1.HolidayCalendar\"m\n\x1dUpdateHolidayCalendarResponse\x12L\n\x10holiday_calendar\x18\x01 \x01(\x0b\x32\x32.connamara.ep3.instruments.v1beta1.HolidayCalendar\"\'\n\x19GetHolidayCalendarRequest\x12\n\n\x02id\x18\x01 \x01(\t\"j\n\x1aGetHolidayCalendarResponse\x12L\n\x10holiday_calendar\x18\x01 \x01(\x0b\x32\x32.connamara.ep3.instruments.v1beta1.HolidayCalendar\"*\n\x1c\x44\x65leteHolidayCalendarRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x1f\n\x1d\x44\x65leteHolidayCalendarResponse2\xc5\x1b\n\x0eInstrumentsAPI\x12\x81\x01\n\x0cListProducts\x12\x36.connamara.ep3.instruments.v1beta1.ListProductsRequest\x1a\x37.connamara.ep3.instruments.v1beta1.ListProductsResponse\"\x00\x12\x84\x01\n\rCreateProduct\x12\x37.connamara.ep3.instruments.v1beta1.CreateProductRequest\x1a\x38.connamara.ep3.instruments.v1beta1.CreateProductResponse\"\x00\x12\x84\x01\n\rUpdateProduct\x12\x37.connamara.ep3.instruments.v1beta1.UpdateProductRequest\x1a\x38.connamara.ep3.instruments.v1beta1.UpdateProductResponse\"\x00\x12{\n\nGetProduct\x12\x34.connamara.ep3.instruments.v1beta1.GetProductRequest\x1a\x35.connamara.ep3.instruments.v1beta1.GetProductResponse\"\x00\x12\x84\x01\n\rDeleteProduct\x12\x37.connamara.ep3.instruments.v1beta1.DeleteProductRequest\x1a\x38.connamara.ep3.instruments.v1beta1.DeleteProductResponse\"\x00\x12\x8a\x01\n\x0fListInstruments\x12\x39.connamara.ep3.instruments.v1beta1.ListInstrumentsRequest\x1a:.connamara.ep3.instruments.v1beta1.ListInstrumentsResponse\"\x00\x12~\n\x0bListSymbols\x12\x35.connamara.ep3.instruments.v1beta1.ListSymbolsRequest\x1a\x36.connamara.ep3.instruments.v1beta1.ListSymbolsResponse\"\x00\x12\x84\x01\n\rGetInstrument\x12\x37.connamara.ep3.instruments.v1beta1.GetInstrumentRequest\x1a\x38.connamara.ep3.instruments.v1beta1.GetInstrumentResponse\"\x00\x12\x8d\x01\n\x10\x43reateInstrument\x12:.connamara.ep3.instruments.v1beta1.CreateInstrumentRequest\x1a;.connamara.ep3.instruments.v1beta1.CreateInstrumentResponse\"\x00\x12\xa2\x01\n\x17UpdatePendingInstrument\x12\x41.connamara.ep3.instruments.v1beta1.UpdatePendingInstrumentRequest\x1a\x42.connamara.ep3.instruments.v1beta1.UpdatePendingInstrumentResponse\"\x00\x12\x9f\x01\n\x16UpdateActiveInstrument\x12@.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentRequest\x1a\x41.connamara.ep3.instruments.v1beta1.UpdateActiveInstrumentResponse\"\x00\x12\x8d\x01\n\x10\x44\x65leteInstrument\x12:.connamara.ep3.instruments.v1beta1.DeleteInstrumentRequest\x1a;.connamara.ep3.instruments.v1beta1.DeleteInstrumentResponse\"\x00\x12\x9c\x01\n\x15UpdateInstrumentState\x12?.connamara.ep3.instruments.v1beta1.UpdateInstrumentStateRequest\x1a@.connamara.ep3.instruments.v1beta1.UpdateInstrumentStateResponse\"\x00\x12\x9c\x01\n\x15UpdateInstrumentStats\x12?.connamara.ep3.instruments.v1beta1.UpdateInstrumentStatsRequest\x1a@.connamara.ep3.instruments.v1beta1.UpdateInstrumentStatsResponse\"\x00\x12\x8a\x01\n\x0fUpdateLastPrice\x12\x39.connamara.ep3.instruments.v1beta1.UpdateLastPriceRequest\x1a:.connamara.ep3.instruments.v1beta1.UpdateLastPriceResponse\"\x00\x12\x9c\x01\n\x15UpdateSettlementPrice\x12?.connamara.ep3.instruments.v1beta1.UpdateSettlementPriceRequest\x1a@.connamara.ep3.instruments.v1beta1.UpdateSettlementPriceResponse\"\x00\x12\x93\x01\n\x12UpdateOpenInterest\x12<.connamara.ep3.instruments.v1beta1.UpdateOpenInterestRequest\x1a=.connamara.ep3.instruments.v1beta1.UpdateOpenInterestResponse\"\x00\x12~\n\x0bGetMetadata\x12\x35.connamara.ep3.instruments.v1beta1.GetMetadataRequest\x1a\x36.connamara.ep3.instruments.v1beta1.GetMetadataResponse\"\x00\x12\x92\x01\n\x11ListenInstruments\x12;.connamara.ep3.instruments.v1beta1.ListenInstrumentsRequest\x1a<.connamara.ep3.instruments.v1beta1.ListenInstrumentsResponse\"\x00\x30\x01\x12\x9c\x01\n\x15\x43reateHolidayCalendar\x12?.connamara.ep3.instruments.v1beta1.CreateHolidayCalendarRequest\x1a@.connamara.ep3.instruments.v1beta1.CreateHolidayCalendarResponse\"\x00\x12\x93\x01\n\x12GetHolidayCalendar\x12<.connamara.ep3.instruments.v1beta1.GetHolidayCalendarRequest\x1a=.connamara.ep3.instruments.v1beta1.GetHolidayCalendarResponse\"\x00\x12\x9c\x01\n\x15UpdateHolidayCalendar\x12?.connamara.ep3.instruments.v1beta1.UpdateHolidayCalendarRequest\x1a@.connamara.ep3.instruments.v1beta1.UpdateHolidayCalendarResponse\"\x00\x12\x9c\x01\n\x15\x44\x65leteHolidayCalendar\x12?.connamara.ep3.instruments.v1beta1.DeleteHolidayCalendarRequest\x1a@.connamara.ep3.instruments.v1beta1.DeleteHolidayCalendarResponse\"\x00\x12\x99\x01\n\x14ListHolidayCalendars\x12>.connamara.ep3.instruments.v1beta1.ListHolidayCalendarsRequest\x1a?.connamara.ep3.instruments.v1beta1.ListHolidayCalendarsResponse\"\x00\x42|\n%com.connamara.ep3.instruments.v1beta1B\x13InstrumentsApiProtoP\x01Z\x12instrumentsv1beta1\xa2\x02\x03\x43\x45I\xaa\x02!Connamara.Ep3.Instruments.V1Beta1b\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'connamara.ep3.instruments.v1beta1.instruments_api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.connamara.ep3.instruments.v1beta1B\023InstrumentsApiProtoP\001Z\022instrumentsv1beta1\242\002\003CEI\252\002!Connamara.Ep3.Instruments.V1Beta1'
  _GETMETADATARESPONSE_METADATAENTRY._options = None
  _GETMETADATARESPONSE_METADATAENTRY._serialized_options = b'8\001'
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEMETADATAREQUEST_METADATAENTRY._options = None
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEMETADATAREQUEST_METADATAENTRY._serialized_options = b'8\001'
  _LISTPRODUCTSREQUEST._serialized_start=443
  _LISTPRODUCTSREQUEST._serialized_end=464
  _LISTPRODUCTSRESPONSE._serialized_start=466
  _LISTPRODUCTSRESPONSE._serialized_end=550
  _CREATEPRODUCTREQUEST._serialized_start=552
  _CREATEPRODUCTREQUEST._serialized_end=635
  _CREATEPRODUCTRESPONSE._serialized_start=637
  _CREATEPRODUCTRESPONSE._serialized_end=721
  _UPDATEPRODUCTREQUEST._serialized_start=723
  _UPDATEPRODUCTREQUEST._serialized_end=806
  _UPDATEPRODUCTRESPONSE._serialized_start=808
  _UPDATEPRODUCTRESPONSE._serialized_end=892
  _GETPRODUCTREQUEST._serialized_start=894
  _GETPRODUCTREQUEST._serialized_end=933
  _GETPRODUCTRESPONSE._serialized_start=935
  _GETPRODUCTRESPONSE._serialized_end=1016
  _DELETEPRODUCTREQUEST._serialized_start=1018
  _DELETEPRODUCTREQUEST._serialized_end=1060
  _DELETEPRODUCTRESPONSE._serialized_start=1062
  _DELETEPRODUCTRESPONSE._serialized_end=1085
  _LISTENINSTRUMENTSREQUEST._serialized_start=1087
  _LISTENINSTRUMENTSREQUEST._serialized_end=1113
  _LISTENINSTRUMENTSRESPONSE._serialized_start=1115
  _LISTENINSTRUMENTSRESPONSE._serialized_end=1209
  _GETMETADATAREQUEST._serialized_start=1211
  _GETMETADATAREQUEST._serialized_end=1231
  _GETMETADATARESPONSE._serialized_start=1234
  _GETMETADATARESPONSE._serialized_end=1392
  _GETMETADATARESPONSE_METADATAENTRY._serialized_start=1345
  _GETMETADATARESPONSE_METADATAENTRY._serialized_end=1392
  _GETINSTRUMENTREQUEST._serialized_start=1394
  _GETINSTRUMENTREQUEST._serialized_end=1439
  _GETINSTRUMENTRESPONSE._serialized_start=1441
  _GETINSTRUMENTRESPONSE._serialized_end=1531
  _CREATEINSTRUMENTREQUEST._serialized_start=1533
  _CREATEINSTRUMENTREQUEST._serialized_end=1625
  _CREATEINSTRUMENTRESPONSE._serialized_start=1627
  _CREATEINSTRUMENTRESPONSE._serialized_end=1720
  _DELETEINSTRUMENTREQUEST._serialized_start=1722
  _DELETEINSTRUMENTREQUEST._serialized_end=1770
  _DELETEINSTRUMENTRESPONSE._serialized_start=1772
  _DELETEINSTRUMENTRESPONSE._serialized_end=1798
  _UPDATEPENDINGINSTRUMENTREQUEST._serialized_start=1800
  _UPDATEPENDINGINSTRUMENTREQUEST._serialized_end=1899
  _UPDATEPENDINGINSTRUMENTRESPONSE._serialized_start=1901
  _UPDATEPENDINGINSTRUMENTRESPONSE._serialized_end=2001
  _UPDATEINSTRUMENTSTATEREQUEST._serialized_start=2004
  _UPDATEINSTRUMENTSTATEREQUEST._serialized_end=2229
  _UPDATEINSTRUMENTSTATERESPONSE._serialized_start=2231
  _UPDATEINSTRUMENTSTATERESPONSE._serialized_end=2329
  _UPDATEINSTRUMENTSTATSREQUEST._serialized_start=2332
  _UPDATEINSTRUMENTSTATSREQUEST._serialized_end=2503
  _UPDATEINSTRUMENTSTATSRESPONSE._serialized_start=2505
  _UPDATEINSTRUMENTSTATSRESPONSE._serialized_end=2536
  _UPDATELASTPRICEREQUEST._serialized_start=2539
  _UPDATELASTPRICEREQUEST._serialized_end=2701
  _UPDATELASTPRICERESPONSE._serialized_start=2703
  _UPDATELASTPRICERESPONSE._serialized_end=2728
  _UPDATESETTLEMENTPRICEREQUEST._serialized_start=2731
  _UPDATESETTLEMENTPRICEREQUEST._serialized_end=2901
  _UPDATESETTLEMENTPRICERESPONSE._serialized_start=2903
  _UPDATESETTLEMENTPRICERESPONSE._serialized_end=2934
  _UPDATEOPENINTERESTREQUEST._serialized_start=2937
  _UPDATEOPENINTERESTREQUEST._serialized_end=3084
  _UPDATEOPENINTERESTRESPONSE._serialized_start=3086
  _UPDATEOPENINTERESTRESPONSE._serialized_end=3114
  _LISTINSTRUMENTSREQUEST._serialized_start=3117
  _LISTINSTRUMENTSREQUEST._serialized_end=3473
  _LISTINSTRUMENTSRESPONSE._serialized_start=3476
  _LISTINSTRUMENTSRESPONSE._serialized_end=3607
  _LISTSYMBOLSREQUEST._serialized_start=3609
  _LISTSYMBOLSREQUEST._serialized_end=3629
  _LISTSYMBOLSRESPONSE._serialized_start=3631
  _LISTSYMBOLSRESPONSE._serialized_end=3669
  _UPDATEACTIVEINSTRUMENTREQUEST._serialized_start=3672
  _UPDATEACTIVEINSTRUMENTREQUEST._serialized_end=7486
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEHOURSREQUEST._serialized_start=5041
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEHOURSREQUEST._serialized_end=5136
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEDATESREQUEST._serialized_start=5139
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEDATESREQUEST._serialized_end=5707
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEPRICELIMITREQUEST._serialized_start=5709
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEPRICELIMITREQUEST._serialized_end=5802
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEORDERSIZELIMITREQUEST._serialized_start=5804
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEORDERSIZELIMITREQUEST._serialized_end=5910
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEHIDEMARKETDATAREQUEST._serialized_start=5912
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEHIDEMARKETDATAREQUEST._serialized_end=5967
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEREJECTQUOTESREQUEST._serialized_start=5969
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEREJECTQUOTESREQUEST._serialized_end=6019
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEHOLIDAYCALENDARSREQUEST._serialized_start=6021
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEHOLIDAYCALENDARSREQUEST._serialized_end=6079
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEPRODUCTREQUEST._serialized_start=6081
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEPRODUCTREQUEST._serialized_end=6115
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEMETADATAREQUEST._serialized_start=6118
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEMETADATAREQUEST._serialized_end=6310
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEMETADATAREQUEST_METADATAENTRY._serialized_start=1345
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEMETADATAREQUEST_METADATAENTRY._serialized_end=1392
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEPOSITIONLIMITREQUEST._serialized_start=6312
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATEPOSITIONLIMITREQUEST._serialized_end=6364
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATETYPEATTRIBUTESREQUEST._serialized_start=6367
  _UPDATEACTIVEINSTRUMENTREQUEST_UPDATETYPEATTRIBUTESREQUEST._serialized_end=7486
  _UPDATEACTIVEINSTRUMENTRESPONSE._serialized_start=7488
  _UPDATEACTIVEINSTRUMENTRESPONSE._serialized_end=7587
  _LISTHOLIDAYCALENDARSREQUEST._serialized_start=7589
  _LISTHOLIDAYCALENDARSREQUEST._serialized_end=7618
  _LISTHOLIDAYCALENDARSRESPONSE._serialized_start=7620
  _LISTHOLIDAYCALENDARSRESPONSE._serialized_end=7729
  _CREATEHOLIDAYCALENDARREQUEST._serialized_start=7731
  _CREATEHOLIDAYCALENDARREQUEST._serialized_end=7839
  _CREATEHOLIDAYCALENDARRESPONSE._serialized_start=7841
  _CREATEHOLIDAYCALENDARRESPONSE._serialized_end=7950
  _UPDATEHOLIDAYCALENDARREQUEST._serialized_start=7952
  _UPDATEHOLIDAYCALENDARREQUEST._serialized_end=8060
  _UPDATEHOLIDAYCALENDARRESPONSE._serialized_start=8062
  _UPDATEHOLIDAYCALENDARRESPONSE._serialized_end=8171
  _GETHOLIDAYCALENDARREQUEST._serialized_start=8173
  _GETHOLIDAYCALENDARREQUEST._serialized_end=8212
  _GETHOLIDAYCALENDARRESPONSE._serialized_start=8214
  _GETHOLIDAYCALENDARRESPONSE._serialized_end=8320
  _DELETEHOLIDAYCALENDARREQUEST._serialized_start=8322
  _DELETEHOLIDAYCALENDARREQUEST._serialized_end=8364
  _DELETEHOLIDAYCALENDARRESPONSE._serialized_start=8366
  _DELETEHOLIDAYCALENDARRESPONSE._serialized_end=8397
  _INSTRUMENTSAPI._serialized_start=8400
  _INSTRUMENTSAPI._serialized_end=11925
# @@protoc_insertion_point(module_scope)