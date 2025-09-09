import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = {
	healthy: '#22c55e', // green
	mild: '#fde047',   // yellow
	infected: '#ef4444', // red
};

const PlantGrid = ({ plants }) => {
	// Count health status for chart
	const healthCounts = plants.reduce(
		(acc, plant) => {
			acc[plant.healthStatus] = (acc[plant.healthStatus] || 0) + 1;
			return acc;
		},
		{ healthy: 0, mild: 0, infected: 0 }
	);

	const chartData = [
		{ name: 'Healthy', value: healthCounts.healthy, color: COLORS.healthy },
		{ name: 'Mildly Infected', value: healthCounts.mild, color: COLORS.mild },
		{ name: 'Infected', value: healthCounts.infected, color: COLORS.infected },
	];

	return (
		<div className="bg-white rounded-xl shadow p-6 border border-green-200">
			<h2 className="text-xl font-semibold text-green-600 mb-4">Plant Health Visualization</h2>
			<div className="mb-6">
				<ResponsiveContainer width="100%" height={200}>
					<PieChart>
						<Pie
							data={chartData}
							dataKey="value"
							nameKey="name"
							cx="50%"
							cy="50%"
							outerRadius={60}
							label
						>
							{chartData.map((entry, index) => (
								<Cell key={`cell-${index}`} fill={entry.color} />
							))}
						</Pie>
						<Tooltip />
						<Legend />
					</PieChart>
				</ResponsiveContainer>
			</div>
			<div className="grid grid-cols-10 gap-2">
				{plants.map((plant) => (
					<div
						key={plant.id}
						className={`w-7 h-7 rounded border flex items-center justify-center text-xs font-bold ${
							plant.healthStatus === 'infected'
								? 'bg-red-300 border-red-500 text-red-900'
								: plant.healthStatus === 'mild'
								? 'bg-yellow-200 border-yellow-400 text-yellow-800'
								: 'bg-green-200 border-green-400 text-green-800'
						}`}
						title={`Plant ${plant.id}: ${plant.healthStatus}`}
					>
						{plant.id}
					</div>
				))}
			</div>
		</div>
	);
};

export default PlantGrid;
