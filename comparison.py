# Edge Comparison with improved accuracy
def edge_compare_v2(canny_string_1, canny_string_2):
    try:
        prep_1 = canny_string_1.split(",")
        prep_2 = canny_string_2.split(",")

        hit = 0
        miss_1 = 0
        miss_2 = 0

        for i in range(len(prep_1)):

            if prep_1[i] == "1":
                if prep_2[i] == "1":
                    hit += 1
                else:
                    miss_1 += 1
            elif prep_2[i] == "1":
                miss_2 += 1

        base_1_score = hit / (hit+miss_1)
        base_2_score = hit / (hit+miss_2)

        return (base_1_score + base_2_score) / 2

    except:
        return 0


def compare_list(canny_string_list):
    for i in range(len(canny_string_list)):
        for j in range(i+1, len(canny_string_list)):
            img_name_1 = canny_string_list[i][0]
            img_name_2 = canny_string_list[j][0]

            img_canny_1 = canny_string_list[i][1]
            img_canny_2 = canny_string_list[j][1]

            info_text = "Comparing \"" + img_name_1 + "\" and \"" + img_name_2 + "\""

            if len(info_text) >= 46:
                info_text = info_text[0:46] + "..."
            print(info_text + (" "*(50-len(info_text))), end="")

            similarity = edge_compare_v2(img_canny_1, img_canny_2)

            if similarity >= .6:
                print("- finished. " + str(int(round(similarity, 2)*100)) + "% Similar!")
            else:
                print("- finished.")

