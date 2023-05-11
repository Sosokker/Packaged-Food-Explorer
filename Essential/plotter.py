import webbrowser
import plotly.graph_objects as go
import plotly.io as pio
import tempfile

class plotter:
    def nutrient_plotter(self, df, row_index, nutrient_indices, chart_type, popup=True, to_html_str=False):
        """
        Generate and display a Plotly graph of nutrient values for a specific row in a DataFrame.

        Parameters:
            df (pandas.DataFrame): The DataFrame containing the nutrient data.
            row_index (int): The index of the row in the DataFrame to plot.
            nutrient_indices (list of int): The column indices of the nutrients to plot.
            chart_type (str): The type of chart to generate ('bar' or 'pie').

        Returns:
            bytes (html_encoded string)

        Raises:
            ValueError: If an invalid chart type is provided.

        Usage:
            nutrient_plotter(df, 0, [16, 18, 20, 22], 'bar')

        NOTE: To embed in tkinter use this code block
        ```py
        import io
        from PIL import Image

        en_html = nutrient_plotter(df, 1, [16, 18, 20, 22], 'bar', to_html_str=True)
        stream = io.BytesIO(str_html)
        image = Image.open(stream)
        photo = tk.PhotoImage(image)
        label = tk.Label(root, image=photo)
        label.pack()
        ```

        """
        product_name = df.iloc[row_index, 1]
        nutrient_values = df.iloc[row_index, nutrient_indices].fillna(0).astype(float)
        nutrient_names = df.columns[nutrient_indices]

        if chart_type == 'bar':
            fig = go.Figure(data=go.Bar(x=nutrient_names, y=nutrient_values, marker_color='skyblue'))
            fig.update_layout(title=f'Nutrient Values for {product_name}', xaxis_title='Nutrients',
                            yaxis_title='Value')
        elif chart_type == 'pie':
            fig = go.Figure(data=go.Pie(labels=nutrient_names, values=nutrient_values))
            fig.update_layout(title=f'Nutrient Composition for {product_name}')
        else:
            raise ValueError('Invalid chart type. Please choose either "bar" or "pie".')

        html_string = pio.to_html(fig, include_plotlyjs='cdn', full_html=False)
        encoded_html = html_string.encode('utf-8')

        if popup:
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp:
                filename = temp.name
                temp.write(encoded_html)

            webbrowser.open(filename)
        if to_html_str:
            return encoded_html

# print(type(nutrient_plotter(df, 1, [16, 18, 20, 22], 'bar', False, True)))