def update_context(app, context_dict):
	if 'KONCH_CONTEXT' in app.config:
		app.config['KONCH_CONTEXT'].update(context_dict)
	else:
		app.config.update({'KONCH_CONTEXT': context_dict})