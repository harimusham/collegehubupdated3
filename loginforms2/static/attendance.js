
document.addEventListener("DOMContentLoaded", function() {
    fetch('/get_stu_atten')
        .then(response => response.json())
        .then(data => {
            var studentData = [];
            data.forEach(row => {
                studentData.push({ id: row[0], attendance: row[1] });
            });

            var studentNames = studentData.map(student => student.id);
            var attendanceData = studentData.map(student => student.attendance);

            var ctx = document.getElementById('attendanceChart').getContext('2d');
            var attendanceChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: studentNames,
                    datasets: [{
                        label: 'Attendance',
                        data: attendanceData,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                max: 100
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Attendance (%)'
                            }
                        }],
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Students'
                            }
                        }]
                    },
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Student Attendance'
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});
