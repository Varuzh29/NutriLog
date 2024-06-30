def food_items_to_html(food_items, no_image_url):
    result = ""

    for food_item in food_items:
        result += f"""
                        <div class="food-card">
                            <div class="food-card-image">
                                <img src="{ food_item['image_url'] or no_image_url }">
                                <h3>{ food_item['name'].title() }</h3>
                            </div>
                            <div class="food-card-content">
                                <table class="tbl">
                                    <tr>
                                        <td>Calories:</td>
                                        <td>{ food_item['kcal'] } kcal</td>
                                        <td rowspan="4">per 100g</td>
                                    </tr>
                                    <tr>
                                        <td>Carbs:</td>
                                        <td>{ food_item['carbohydrates'] } g</td>
                                    </tr>
                                    <tr>
                                        <td>Fat:</td>
                                        <td>{ food_item['fat'] } g</td>
                                    </tr>
                                    <tr>
                                        <td>Protein:</td>
                                        <td>{ food_item['protein'] } g</td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                            """
    return result
