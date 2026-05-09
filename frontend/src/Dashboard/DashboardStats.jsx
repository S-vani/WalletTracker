function DashboardStats({stats}) {
    return (
        <div>
            <h3>{stats.value}</h3>
            <h3>{stats.curr_timeperiod}</h3>
        </div>
    )
}

export default DashboardStats
