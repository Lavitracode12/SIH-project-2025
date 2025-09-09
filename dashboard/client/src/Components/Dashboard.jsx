import React, { useEffect, useState } from 'react';
import PlantGrid from './PlantGrid';

const Dashboard = () => {
	// Dynamic data from backend
	const [overview, setOverview] = useState({
		totalPlants: 0,
		infectedPlants: 0,
		pesticideUsed: 0,
	});
	const [plants, setPlants] = useState([]); // [{id, healthStatus}]
	const [notifications, setNotifications] = useState([]);
	const [sprayerStatus, setSprayerStatus] = useState('inactive');

	useEffect(() => {
		// Fetch data from backend API
		// Example endpoints: /api/overview, /api/plants, /api/notifications, /api/sprayer
		// Replace with your actual API calls
		const fetchData = async () => {
			try {
				const overviewRes = await fetch('/api/overview');
				const overviewData = await overviewRes.json();
				setOverview(overviewData);

				const plantsRes = await fetch('/api/plants');
				const plantsData = await plantsRes.json();
				setPlants(plantsData);

				const notificationsRes = await fetch('/api/notifications');
				const notificationsData = await notificationsRes.json();
				setNotifications(notificationsData);

				const sprayerRes = await fetch('/api/sprayer');
				const sprayerData = await sprayerRes.json();
				setSprayerStatus(sprayerData.status);
			} catch (err) {
				// Handle errors
			}
		};
		fetchData();
	}, []);

	// Sprayer control handlers
	const handleSprayer = async (action) => {
		await fetch(`/api/sprayer/${action}`, { method: 'POST' });
		setSprayerStatus(action === 'start' ? 'active' : 'inactive');
	};

	return (
		<div className="min-h-screen bg-gradient-to-br from-white to-green-100 p-6 font-sans">
			<h1 className="text-3xl font-bold text-green-700 mb-6 text-center">Intelligent Pesticide Sprinkling System</h1>
			<div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
				<section className="bg-white rounded-xl shadow p-6 border border-green-200">
					<h2 className="text-xl font-semibold text-green-600 mb-4">Overview</h2>
					<ul className="space-y-2 text-green-800">
						<li>Total Plants Monitored: <span className="font-bold">{overview.totalPlants}</span></li>
						<li>Infected Plants: <span className="font-bold">{overview.infectedPlants}</span></li>
						<li>Pesticide Used Today: <span className="font-bold">{overview.pesticideUsed} L</span></li>
					</ul>
				</section>
				<section className="col-span-2">
					<PlantGrid plants={plants} />
				</section>
				<section className="bg-white rounded-xl shadow p-6 border border-green-200">
					<h2 className="text-xl font-semibold text-green-600 mb-4">Sprayer Control</h2>
					<div className="flex gap-4 mb-2">
						<button
							className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
							onClick={() => handleSprayer('start')}
							disabled={sprayerStatus === 'active'}
						>
							Start Spraying
						</button>
						<button
							className="px-4 py-2 bg-gray-300 text-green-700 rounded hover:bg-green-200 transition"
							onClick={() => handleSprayer('stop')}
							disabled={sprayerStatus === 'inactive'}
						>
							Stop Spraying
						</button>
					</div>
					<div className="text-green-800">Status: <span className="font-bold">{sprayerStatus}</span></div>
				</section>
			</div>
			<div className="bg-white rounded-xl shadow p-6 border border-green-200 max-w-2xl mx-auto">
				<h2 className="text-xl font-semibold text-green-600 mb-4">Notifications</h2>
				<ul className="space-y-2">
					{notifications.length === 0 ? (
						<li className="text-gray-500">No notifications</li>
					) : (
						notifications.map((note, idx) => (
							<li key={idx} className="text-green-800">{note}</li>
						))
					)}
				</ul>
			</div>
		</div>
	);
};

export default Dashboard;
