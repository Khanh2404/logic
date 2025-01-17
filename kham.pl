% Cơ sở tri thức về triệu chứng và bệnh
% Bệnh về Mắt
benh(viem_ket_mac, [mat_do, mat_ngua, mat_cay]).
benh(cuom_nuoc, [mat_nho_nuoc, mat_mo, mat_dau]).
benh(loet_giac_mac, [mat_dau, mat_cay, mat_mo]).


% Bệnh về Tai
benh(viem_tai_giua, [tai_dau, tai_nghe_kem, sot]).
benh(roi_loai_thinh_luc, [tai_nghe_kem, mat_can_bang, u_tai]).
benh(viem_tai_ngoai, [tai_sung, tai_dau, u_tai]).

% Bệnh về Mũi
benh(viem_xoang, [mui_tac, mui_nhot, dau_dau]).
benh(viem_mui_di_ung, [mui_ngua, mui_tac, hat_xi]).
benh(polyp_mui, [mui_tac, mat_khuu_giac, dau_dau]).

% Bệnh về Họng
benh(viem_hong_cap, [hong_dau, sot, nuot_kho]).
benh(ung_thu_vom_hong, [hong_dau, sot, nuot_dau]).
benh(viem_amidan, [hong_dau, ho, khan_tieng]).

% Trọng số cho triệu chứng
trong_so(mat_do, 0.2).
trong_so(mat_ngua, 0.1).
trong_so(mat_cay, 0.1).
trong_so(mat_nho_nuoc, 0.2).
trong_so(mat_mo, 0.2).
trong_so(mat_dau, 0.2).
trong_so(tai_dau, 0.2).
trong_so(tai_nghe_kem, 0.2).
trong_so(sot, 0.1).
trong_so(mat_can_bang, 0.1).
trong_so(u_tai, 0.1).
trong_so(tai_sung, 0.1).
trong_so(mui_tac, 0.2).
trong_so(mui_nhot, 0.1).
trong_so(dau_dau, 0.2).
trong_so(mui_ngua, 0.1).
trong_so(hat_xi, 0.1).
trong_so(mat_khuu_giac, 0.1).
trong_so(hong_dau, 0.2).
trong_so(nuot_kho, 0.1).
trong_so(nuot_dau, 0.1).
trong_so(ho, 0.1).
trong_so(khan_tieng, 0.1).


filter_non_zero([], []).
filter_non_zero([(Benh, PhanTram)|T], [(Benh, PhanTram)|T2]) :-
    PhanTram > 0,
    filter_non_zero(T, T2).
filter_non_zero([(_, PhanTram)|T], T2) :-
    PhanTram =< 0,
    filter_non_zero(T, T2).


tinh_phan_tram(Benh, PhanTram) :-
    benh(Benh, TrieuChungBenh),
    findall(TongTrongSo, (
        member(Tri, TrieuChungBenh),
        trieu_chung(Tri),
        trong_so(Tri, TrongSo),
        TongTrongSo is TrongSo
    ), TrongSoList),
    sum_list(TrongSoList, TongTrongSo),
    length(TrieuChungBenh, TongSoTrieuChung),
    ( TongSoTrieuChung = 0 ->
      PhanTram = 0
    ; PhanTram is (TongTrongSo / TongSoTrieuChung) * 100
    ).

% Kết hợp hai danh 
zip([], [], []).
zip([H1|T1], [H2|T2], [(H1, H2)|T3]) :-
    zip(T1, T2, T3).


tinh_tat_ca :-
    findall(Benh, benh(Benh, _), BenhList),
    maplist(tinh_phan_tram, BenhList, PhanTramList),
    zip(BenhList, PhanTramList, BenhPhanTramList),
    filter_non_zero(BenhPhanTramList, FilteredList),
    ( FilteredList = [] ->
        write('Ban hay nhap benh hoac chon dung lai khong kham nua.'), nl
    ; msort(FilteredList, SortedList),
      print_separator,
      print_sorted(SortedList),
      print_separator,
      ( SortedList = [(BenhMax, MaxPhanTram)|_],
        findall(P, member((_,P), SortedList), PhanTramList2),
        list_to_set(PhanTramList2, SetPhanTramList2),
        ( SetPhanTramList2 = [MaxPhanTram] ->
            format('Ket luan: Benh: ~w~n', [BenhMax]),
            print_separator,
            write('Len di gap bac si de biet them chi tiet.'), nl
        ; format('Ket luan: Benh: ~w~n', [BenhMax]),
            print_separator,
            write('Len di gap bac si de biet them chi tiet.'), nl
        )
      )
    ).


print_sorted([]).
print_sorted([(Benh, PhanTram)|T]) :-
    format('~w: ~2f%~n', [Benh, PhanTram]),
    print_sorted(T).
print_separator :-
    format('~n--------------------~n').



valid_symptom(mat_do).
valid_symptom(mat_ngua).
valid_symptom(mat_cay).
valid_symptom(mat_nho_nuoc).
valid_symptom(mat_mo).
valid_symptom(mat_dau).
valid_symptom(tai_dau).
valid_symptom(tai_nghe_kem).
valid_symptom(sot).
valid_symptom(mat_can_bang).
valid_symptom(u_tai).
valid_symptom(tai_sung).
valid_symptom(mui_tac).
valid_symptom(mui_nhot).
valid_symptom(dau_dau).
valid_symptom(mui_ngua).
valid_symptom(hat_xi).
valid_symptom(mat_khuu_giac).
valid_symptom(hong_dau).
valid_symptom(nuot_kho).
valid_symptom(nuot_dau).
valid_symptom(ho).
valid_symptom(khan_tieng).


doc_trieu_chung :-
    read(Trieu_chung),
    ( Trieu_chung = xong ->
        true  % Nếu người dùng nhập "xong", dừng lại
    ; valid_symptom(Trieu_chung) ->
        assert(trieu_chung(Trieu_chung)),  % Lưu triệu chứng vào cơ sở dữ liệu
        doc_trieu_chung  % Tiếp tục đọc các triệu chứng khác
    ;   write('Trieu chung khong hop le. Vui long nhap lai.'), nl,
        doc_trieu_chung  % Yêu cầu nhập lại triệu chứng
    ).


    
bat_dau :-
    write('Nhap tung trieu chung (ket thuc bang "xong"): '), nl,
    doc_trieu_chung,
    tinh_tat_ca,  % Gọi hàm tính tất cả các tỷ lệ phần trăm
    retractall(trieu_chung(_)).  % Xóa hết các triệu chứng đã nhập sau khi hoàn tất

