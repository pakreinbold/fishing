import tensorflow as tf
import plotly.graph_objects as go


if __name__ == '__main__':
    x = tf.linspace(-1, 1, 250)
    y = (x**2 - 1)**4
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode='lines'
        )
    )
    fig.update_layout(
        template='simple_white', width=1200, height=800,
        xaxis_title='$x$', yaxis_title='$y$'
    )
    fig.show()
