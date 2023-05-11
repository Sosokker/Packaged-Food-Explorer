import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import tempfile
import tkinter as tk
import webview
from PIL import Image, ImageTk

class plotter:
    def nutrient_plotter(self, df, row_index, nutrient_indices, chart_type, popup=True, frame=None):
        """
        Generate and display a Plotly graph of nutrient values for a specific row in a DataFrame.

        Parameters:
            df (pandas.DataFrame): The DataFrame containing the nutrient data.
            row_index (int): The index of the row in the DataFrame to plot.
            nutrient_indices (list of int): The column indices of the nutrients to plot.
            chart_type (str): The type of chart to generate ('bar' or 'pie').
            popup (bool): to ask if you want to popup new webview window or embed to gui

        Returns:
            bytes (html_encoded string)

        Raises:
            ValueError: If an invalid chart type is provided.

        Usage:
            nutrient_plotter(df, 0, [16, 18, 20, 22], 'bar')
        ```

        """
        product_name = df.iloc[row_index, 1]
        nutrient_values = df.iloc[row_index, nutrient_indices].fillna(0).astype(float)
        nutrient_names = df.columns[nutrient_indices]

        if chart_type == 'bar':
            fig = go.Figure(data=go.Bar(x=nutrient_names, y=nutrient_values, marker_color='skyblue'))
            fig.update_layout(title='Macronutrients Graph',xaxis_title='Nutrients',
                            yaxis_title='Value')
        elif chart_type == 'pie':
            fig = go.Figure(data=go.Pie(labels=nutrient_names, values=nutrient_values))
            fig.update_layout(title=f'Nutrient of {product_name}')
        elif chart_type == 'barpie':
            fig = make_subplots(rows=2, cols=2, specs=[[{"type": "xy"}, {"type": "domain"}], [{}, {}]])
            fig.add_trace(go.Pie(labels=nutrient_names, values=nutrient_values),
                          row=1, col=2)
            fig.add_trace(go.Bar(x=nutrient_names, y=nutrient_values, marker_color='skyblue'),
                          row=1, col=1)
            fig.update_layout(title=f'Nutrient of {product_name}')
        else:
            raise ValueError('Invalid chart type. Please choose either "bar" or "pie" or "barpie".')

        html_string = pio.to_html(fig, include_plotlyjs='cdn', full_html=False)
        encoded_html = html_string.encode('utf-8')

        if popup:
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp:
                filename = temp.name
                print(filename)
                temp.write(encoded_html)
            temp.close()
            webview.create_window('Nutrients Graph', filename)
            webview.start()
            os.remove(filename)
        else:
            fig.update_layout(width=350, height=300)
            temp_dir = tempfile.mkdtemp()
            image_path = os.path.join(temp_dir, "plot.jpeg")
            fig.write_image(image_path, format="jpeg")
            label = tk.Label(frame)
            img = Image.open(image_path)
            label.img = ImageTk.PhotoImage(img)
            label['image'] = label.img
            label.pack()
            os.remove(image_path)

# print(type(nutrient_plotter(df, 1, [16, 18, 20, 22], 'bar', False, True)))