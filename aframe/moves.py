import numpy as np
import func as f

# key times (seconds) from the video cooresponding to key moves
key_times = [1, 3, 8, 15, 18, 20, 22]

# coordinates of each key point cooresponding to a key time
key_coords = [[(0.5823251008987427, 0.20194004476070404), (0.48124122619628906, 0.19683437049388885), (0.6375653147697449, 0.14787273108959198), (0.4278026521205902, 0.15780885517597198), (0.6456394195556641, 0.04710020869970322), (0.4214968979358673, 0.05645260959863663), (0.5537256598472595, 0.42983537912368774), (0.5010578036308289, 0.4291539192199707), (0.5523173213005066, 0.6019559502601624), (0.49470609426498413, 0.598834216594696), (0.5576156377792358, 0.7320566773414612), (0.4953809380531311, 0.7297883033752441)], [(0.5823169946670532, 0.20970556139945984), (0.483795166015625, 0.2069086879491806), (0.6428315043449402, 0.1951870173215866), (0.42361265420913696, 0.21148626506328583), (0.6529965400695801, 0.09424566477537155), (0.40368980169296265, 0.11877825856208801), (0.5538366436958313, 0.4328016936779022), (0.5015226006507874, 0.42894595861434937), (0.5515636205673218, 0.6035171747207642), (0.49427875876426697, 0.6030696034431458), (0.5575175285339355, 0.7314013242721558), (0.4958939254283905, 0.7292580604553223)], [(0.5902402400970459, 0.2105710804462433), (0.49275118112564087, 0.21131795644760132), (0.6505895256996155, 0.22453008592128754), (0.43804052472114563, 0.25065475702285767), (0.6502930521965027, 0.1293719857931137), (0.4229501783847809, 0.15086138248443604), (0.5609538555145264, 0.42868342995643616), (0.507880687713623, 0.4241883158683777), (0.5572041869163513, 0.5998584628105164), (0.4975775182247162, 0.5977992415428162), (0.558937668800354, 0.7338120341300964), (0.49525704979896545, 0.7345379590988159)], [(0.6137027740478516, 0.21499456465244293), (0.5186814069747925, 0.215302973985672), (0.631131112575531, 0.3211475908756256), (0.49335619807243347, 0.3179803490638733), (0.6454318165779114, 0.40386873483657837), (0.5040892362594604, 0.3849358558654785), (0.575182318687439, 0.44246017932891846), (0.52015620470047, 0.4320646822452545), (0.5639507174491882, 0.5930470824241638), (0.492085725069046, 0.5579615831375122), (0.5566032528877258, 0.7362147569656372), (0.47204214334487915, 0.7105807065963745)], [(0.5216461420059204, 0.18715211749076843), (0.4330351650714874, 0.2023717612028122), (0.5660487413406372, 0.1884009689092636), (0.3788057565689087, 0.237638920545578), (0.4974610507488251, 0.1938621699810028), (0.44283920526504517, 0.2118472158908844), (0.54462730884552, 0.3818003833293915), (0.4988378584384918, 0.4246733784675598), (0.6468709111213684, 0.4067765474319458), (0.5002850294113159, 0.5817511677742004), (0.7466593384742737, 0.4355268180370331), (0.5026950240135193, 0.73204505443573)], [(0.6109994053840637, 0.20306560397148132), (0.519324004650116, 0.2025524377822876), (0.6614972352981567, 0.26986706256866455), (0.4805826246738434, 0.26109832525253296), (0.5885016918182373, 0.23318135738372803), (0.5443659424781799, 0.22318358719348907), (0.5598015189170837, 0.4328095614910126), (0.5112913250923157, 0.40308231115341187), (0.5449583530426025, 0.5811640024185181), (0.43119487166404724, 0.3924829661846161), (0.5381781458854675, 0.7343194484710693), (0.4411109685897827, 0.5606743097305298)], [(0.5385665893554688, 0.20647718012332916), (0.44563180208206177, 0.2048627883195877), (0.5801581740379333, 0.2724149823188782), (0.4121205508708954, 0.26323872804641724), (0.5195841789245605, 0.24323678016662598), (0.4794417917728424, 0.23432651162147522), (0.5270692110061646, 0.42614975571632385), (0.47279754281044006, 0.43259748816490173), (0.5387643575668335, 0.5789867043495178), (0.4773072898387909, 0.5992333889007568), (0.5394235849380493, 0.7286103963851929), (0.49410519003868103, 0.7386519312858582)]]

# angles cooresponding to the coordinates
key_angles = [
    [
        f.angle(np.array(key_coords[i][0]), np.array(key_coords[i][2]), np.array(key_coords[i][4])),
        f.angle(np.array(key_coords[i][1]), np.array(key_coords[i][3]), np.array(key_coords[i][5])),
        f.angle(np.array(key_coords[i][6]), np.array(key_coords[i][0]), np.array(key_coords[i][2])),
        f.angle(np.array(key_coords[i][7]), np.array(key_coords[i][1]), np.array(key_coords[i][3])),
        f.angle(np.array(key_coords[i][6]), np.array(key_coords[i][8]), np.array(key_coords[i][10])),
        f.angle(np.array(key_coords[i][7]), np.array(key_coords[i][9]), np.array(key_coords[i][11])),
        f.angle(np.array(key_coords[i][0]), np.array(key_coords[i][6]), np.array(key_coords[i][8])),
        f.angle(np.array(key_coords[i][1]), np.array(key_coords[i][7]), np.array(key_coords[i][9]))
    ]
    for i in range(len(key_times))
]

print(key_angles)