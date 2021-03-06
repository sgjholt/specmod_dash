# -*- coding: utf-8 -*-

"""
specplot.py

	The file with functions to style the spectral plots.
"""

import numpy as np
import plotly.graph_objects as go
from SpecMod.specmod.Spectral import Spectra, SNP
from typing import Tuple

def get_min_max_freqs(snp: SNP) -> Tuple[np.ndarray, np.ndarray]:
	"""
	Gets minimum and maximum frequencies from 

	"""
	mn, mx = np.log10([np.round(snp.signal.freq[1], 1), 
	       np.round(snp.signal.freq[-1], 1)])
	return mn, mx


def get_marks(mn: np.ndarray, 
	          mx: np.ndarray, 
	          n: int = 10):
	marks = {i: '{}Hz'.format(np.round(10 ** i, 1)) for i in np.linspace(mn, mx, n)}
	return marks


def get_band_vals(snp):

	value = get_min_max_freqs(snp)


	try:
		value = np.log10([np.round(snp.ubfreqs[0], 1), 
			         np.round(snp.ubfreqs[1], 1)])

	except IndexError:
		pass

	return value



def make_fig(sfreq, samp, nfreq, namp, pass_snr, vals):

	fac=1.25

	fig = go.Figure()

	fig.add_trace(
		go.Scatter(
			x=nfreq, 
			y=namp, 
			mode='lines', 
			name='noise'
			)
		)

	fig.add_trace(
		go.Scatter(
			x=sfreq, 
			y=samp, 
			mode='lines', 
			name='signal'
			)
		)

	print(vals)

	if vals is not None and pass_snr:
		for val, sv in zip(vals, [True, False]):
			fig.add_trace(
				go.Scatter(
					x=[10**val, 10**val], 
					y=[np.min([samp.min()/fac, 
					   namp.min()/fac]), 
				       np.max([samp.max()*fac, 
					   namp.max()*fac])
					   ], 
					mode='lines',
					line_width=2,
					line_color='black', 
					name="bandwidth", 
					legendgroup="bd",
                    showlegend=sv
					),
				)

	fig.update_layout(
		font_family="Times New Roman",
		xaxis_title="Frequency (Hz)",
		yaxis_title="Spec. Vel. ([m/s] s)",
		xaxis_type="log", 
		yaxis_type="log", 
		yaxis_range=[
			np.min([np.log10(samp.min()/fac), 
				np.log10(namp.min()/fac)]), 
			np.max([np.log10(samp.max()*fac), 
				np.log10(namp.max()*fac)])
			],
		xaxis_range=[
			np.min([np.log10(sfreq.min()/fac), 
				np.log10(nfreq.min()/fac)]), 
			np.max([np.log10(sfreq.max()*fac), 
				np.log10(nfreq.max()*fac)])
			],
		
        legend=dict(
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                orientation='h'
            )
	   )

	return fig