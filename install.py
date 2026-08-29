import questionary


tra_loi = questionary.confirm("Og có muốn tiếp tục không?").ask()

if tra_loi:
    print("Og đã chọn YES! :)")
else:
    print("Og đã chọn NO! :)")