from vnaddress import VNAddressStandardizer
address = VNAddressStandardizer(raw_address = "Tổ dân phô 15, thị trấn cẩm xuyên,hà tĩnh", comma_handle = True,detail=True)
#print(address.execute())
print(address.combined_processing(raw_address = "Tổ dân phô 15, thị trấn cẩm xuyên,hà tĩnh"))
