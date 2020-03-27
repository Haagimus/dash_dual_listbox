from dash_dual_listbox.DualList import DualList
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

app = dash.Dash('')
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.layout = dbc.Row([
    dbc.Col([
        dbc.Row(
            dcc.Dropdown(id='pgm-admin-dd-left',
                         className='pgm-admin-dd',
                         options=[{'label': 'One', 'value': '1'},
                                  {'label': 'Two', 'value': '2'},
                                  {'label': 'Three', 'value': '3'},
                                  {'label': 'Four', 'value': '4'},
                                  {'label': 'Five', 'value': '5'},
                                  {'label': 'Six', 'value': '6'},
                                  {'label': 'Seven', 'value': '7'},
                                  {'label': 'Eight', 'value': '8'},
                                  {'label': 'Nine', 'value': '9'},
                                  {'label': 'Ten', 'value': '10'}],
                         multi=True)),
        dbc.Row(
            html.Select(id='pgm-admin-list-left',
                        className='pgm-admin-list',
                        disabled=True,
                        size=6))],
        className='pgm-admin-container'
    ),
    dbc.Col([
        html.Div(id='buttons',
                 children=[dbc.Row(dbc.Button('>', id='add-one',
                                              className='pgm-admin-button')),
                           dbc.Row(dbc.Button('>>', id='add-all',
                                              className='pgm-admin-button')),
                           dbc.Row(dbc.Button('<', id='remove-one',
                                              className='pgm-admin-button')),
                           dbc.Row(dbc.Button('<<', id='remove-all',
                                              className='pgm-admin-button'))]
                 )],
        className='pgm-admin-button-container'
    ),
    dbc.Col([
        dbc.Row(
            dcc.Dropdown(id='pgm-admin-dd-right',
                         className='pgm-admin-dd',
                         options=[],
                         multi=True)),
        dbc.Row(
            html.Select(id='pgm-admin-list-right',
                        className='pgm-admin-list',
                        disabled=True,
                        size=6))],
        className='pgm-admin-container'
    )
],
    className='pgm-admin-parent')


@app.callback([Output('pgm-admin-dd-left', 'options'),
               Output('pgm-admin-dd-right', 'options'),
               Output('pgm-admin-list-left', 'children'),
               Output('pgm-admin-list-right', 'children')],
              [Input('add-one', 'n_clicks_timestamp'),
               Input('add-all', 'n_clicks_timestamp'),
               Input('remove-one', 'n_clicks_timestamp'),
               Input('remove-all', 'n_clicks_timestamp')],
              [State('pgm-admin-dd-left', 'value'),
               State('pgm-admin-dd-right', 'value'),
               State('pgm-admin-list-left', 'children'),
               State('pgm-admin-list-right', 'children')])
def move_items(add_one, add_all, rem_one, rem_all, left_dd, right_dd, left_list, right_list):
    add_one = 0 if add_one is None else add_one
    add_all = 0 if add_all is None else add_all
    rem_one = 0 if rem_one is None else rem_one
    rem_all = 0 if rem_all is None else rem_all

    opts = [('One', '1'),
            ('Two', '2'),
            ('Three', '3'),
            ('Four', '4'),
            ('Five', '5'),
            ('Six', '6'),
            ('Seven', '7'),
            ('Eight', '8'),
            ('Nine', '9'),
            ('Ten', '10')]

    dd_opts = [{'label': k[0], 'value': k[1]} for k in opts]

    list_opts = [html.Option(k[0], id=k[1]) for k in opts]

    if all(add_one > x for x in (add_all, rem_one, rem_all)):
        l_dd = [x for x in dd_opts if x['value'] not in left_dd]
        r_dd = [x for x in dd_opts if x['value'] in left_dd]
        l_list = [html.Option(x['label'], id=x['value']) for x in l_dd]
        r_list = [html.Option(x['label'], id=x['value']) for x in r_dd]
        return l_dd, r_dd, l_list, r_list
    elif all(add_all > x for x in (add_one, rem_one, rem_all)):
        return [], dd_opts, [], list_opts
    elif all(rem_one > x for x in (add_one, add_all, rem_all)):
        l_dd = [x for x in dd_opts if x['value'] not in right_dd]
        r_dd = [x for x in dd_opts if x['value'] in right_dd]
        l_list = [html.Option(x['label'], id=x['value']) for x in l_dd]
        r_list = [html.Option(x['label'], id=x['value']) for x in r_dd]
        return l_dd, r_dd, l_list, r_list
    elif all(rem_all > x for x in (add_one, add_all, rem_one)):
        return dd_opts, [], list_opts, []
    else:
        return dd_opts, [], list_opts, []


if __name__ == '__main__':
    app.run_server(debug=True)
