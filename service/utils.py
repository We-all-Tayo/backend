class Utils:
    def count_bus(self, bus_dict, target_color):
        same_color = 0
        diff_color = 0

        for _, color in bus_dict.items():
            if color is target_color:
                same_color += 1
            else:
                diff_color += 1
        
        return same_color, diff_color
