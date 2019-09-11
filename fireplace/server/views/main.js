var app = angular.module('myApp', ['ngRoute']).controller('IndexController', function ($scope, $http) {
    $scope.message = 'Hello from IndexController';
    $scope.counterSensors = 0;
    $scope.secondsPerDay = 86400;

    //Base Url for Server
    $scope.base_url_api = '/v1/api';

    //List of SensorNames 
    $scope.SensorList = ["sensor0"];

    //Array for all sensordata
    $scope.SensorData = [];

    $scope.round2decs = function (value) {
        return Math.round(value * 100) / 100;
    }

    //Models
    function SensorInfo(ID, Name, CurrentTemp, DailyAvgTemp, DailyMinTemp, DailyMaxTemp, UltAvgTemp, UltMinTemp, UltMaxTemp, AlertMinTemp, AlertMaxTemp, TTStamps, LastUpdated, interval, latest, offset) {
        this.ID = ID;
        this.Name = Name;
        this.CurrentTemp = CurrentTemp || -1;
        this.DailyAvgTemp = DailyAvgTemp || -1;
        this.DailyMinTemp = DailyMinTemp || -1;
        this.DailyMaxTemp = DailyMaxTemp || -1;
        this.UltAvgTemp = UltAvgTemp || -1;
        this.UltMinTemp = UltMinTemp || -1;
        this.UltMaxTemp = UltMaxTemp || -1;
        this.AlertMinTemp = AlertMinTemp || 0;
        this.AlertMaxTemp = AlertMaxTemp || 50;
        this.TTStamps = TTStamps; //Array +

        this.LastUpdated = LastUpdated;
        this.interval = interval || 28800; //8hours
        this.latest = latest || 8;
        this.offset = offset || 0;
    }

    function TTStamp(Time, AvgTemp, MinTemp, MaxTemp) {
        this.Time = Time;
        this.AvgTemp = AvgTemp;
        this.MinTemp = MinTemp;
        this.MaxTemp = MaxTemp;
    };
    //Models End

    //Create Sensor Objects and fill them with Data from API
    $scope.createSensorObjects = function () {
        $scope.SensorList.forEach(function (Sensor) {
            var SensorName = Sensor.name;
            console.log(SensorName);
            //### First get Daily Max/Min/Avg
            //example: [{"time":"2019-08-28T00:00:00+00:00","min_temperature":20.0,"max_temperature":40.0,"avg_temperature":29.9}]
            var dMinTemp, dMaxTemp, dAvgTemp;
            try {
                var responseDaily = $scope.getSensorDailyUltima(SensorName);
                //round to 2 decimal
                dMinTemp = $scope.round2decs(responseDaily.min_temperature);
                dMaxTemp = $scope.round2decs(responseDaily.max_temperature);
                dAvgTemp = $scope.round2decs(responseDaily.avg_temperature);
            } catch (err) {
                console.log("Error in createSensorObjects/getSensorDailyUltima:" + err);
            }

            //### Get Interval Max/Min/Avg
            var ultMinTemp, ultMaxTemp, ultAvgTemp;
            try {
                var responseAllTime = $scope.getSensorIntervalUltima(SensorName, $scope.secondsPerDay);
                ultMinTemp = $scope.round2decs(responseAllTime.min_temperature);
                ultMaxTemp = $scope.round2decs(responseAllTime.max_temperature);
                ultAvgTemp = $scope.round2decs(responseAllTime.avg_temperature);
                console.log(responseAllTime);
            } catch (err) {
                console.log("Error in createSensorObjects/getSensorAllTimeUltima:" + err);
            }

            //Load 8 values form last 8 hours
            try {
                var vps = $scope.getLast8h8TTStamps(SensorName);
                //basicResponse.forEach( function(valuepair){
                //vps.push(new TTStamp(valuepair.time, valuepair.avg_temperature, valuepair.min_temperature, valuepair.max_temperature));
                //});
            }
            catch (err) {
                console.log("Error in createSensorObjects/pushVPS:" + err);
            }

            //Get CurrentTemp 
            var CurrentTemp = $scope.getSensorCurrentTemp(SensorName);

            //Get Max/Min-TempAlert Values
            var AlertMinTemp = 0; //Not used in Serverraum Monitoring
            var AlertMaxTemp = Sensor.threshold;


            //Create LastUpdated Timestamp
            var dateNow = new Date();
            var LastUpdated = dateNow.getDate() + "/"
                + (dateNow.getMonth() + 1) + "/"
                + dateNow.getFullYear() + " @ "
                + dateNow.getHours() + ":"
                + dateNow.getMinutes() + ":"
                + dateNow.getSeconds();

            //finally construct the object 
            //ID, Name, CurrentTemp, DailyAvgTemp, DailyMinTemp, DailyMaxTemp, UltAvgTemp, UltMinTemp, UltMaxTemp, AlertMinTemp, AlertMaxTemp, TTStamps, LastUpdated, interval, latest, offset
            var SensorInfoObject = new SensorInfo($scope.counterSensors++, SensorName, CurrentTemp, dAvgTemp, dMinTemp, dMaxTemp, ultAvgTemp, ultMinTemp, ultMaxTemp, AlertMinTemp, AlertMaxTemp, vps, LastUpdated, 28800, 8, 0);
            console.log(SensorInfoObject);
            //PUSH IN $SCOPE.SENSORDATA
            $scope.SensorData.push(SensorInfoObject);
            console.log($scope.SensorData);

        });
    }



    //SensorData
    SensorInfo.prototype.mod = function () {
        //var responseDaily = $scope.getSensorDailyUltima(sensorName);
        //get the new requested data from API
        var response = $scope.callAPI($scope.base_url_api, 'GET', this.Name, this.interval, this.latest, this.offset);
        console.log(response)

        try {
            var ttstamps = [];
            response.forEach(function (kvpData) {
                ttstamps.push(new TTStamp(kvpData.time, kvpData.avg_temperature, kvpData.min_temperature, kvpData.max_temperature));
            });

            //Get Interval Min/Max/Avg 
            var responseUlt = $scope.callAPI($scope.base_url_api, 'GET', this.Name, this.interval, 1, this.offset);
            responseUlt.forEach(function (kvpData) {
                this.UltAvgTemp = kvpData.avg_temperature;
                this.UltMinTemp = kvpData.min_temperature;
                this.ultMaxTemp = kvpData.max_temperature;
            });
            //Create LastUpdated Timestamp
            var dateNow = new Date();
            this.LastUpdated = dateNow.getDate() + "/"
                + (dateNow.getMonth() + 1) + "/"
                + dateNow.getFullYear() + " @ "
                + dateNow.getHours() + ":"
                + dateNow.getMinutes() + ":"
                + dateNow.getSeconds();

            console.log(this);
            this.TTStamps = ttstamps
            $scope.updateGraphs();
            return 1;
        } catch (err) {
            console.log(err);
            console.log("Error in SensorData.prototype.mod" + err);
            return null;
        };

    }


    $scope.updateModel = function () {
        console.log("SensorID Check: " + SensorID);
        console.log($scope.SensorData);
    }

    //Get Standart Daily Values for creation
    $scope.getLast8h8TTStamps = function (SensorName) {
        var response = $scope.callAPI($scope.base_url_api, 'GET', SensorName, 3600, 8, 0);
        var ttstamps = [];
        try {
            response.forEach(function (ttstamp) {
                ttstamps.push(new TTStamp(
                    ttstamp.time.slice(0, -6).replace('T', ' @'),
                    $scope.round2decs(ttstamp.avg_temperature),
                    $scope.round2decs(ttstamp.min_temperature),
                    $scope.round2decs(ttstamp.max_temperature)
                ));
            });
            return ttstamps;
        } catch (err) {
            console.log("Error in createSensorObjects/getLast8hTTStamps:" + err);
        }
    }

    //Get Daily Min/Max/Avg
    $scope.getSensorDailyUltima = function (SensorName) {
        var response = $scope.callAPI($scope.base_url_api, 'GET', SensorName, $scope.secondsPerDay, 1, 0);
        try {
            return response[0];
        } catch (err) {
            console.log("Error in createSensorObjects/getSensorDailyUltima:" + err);
        }
    }

    //Interval Min/Max/Avg
    $scope.getSensorIntervalUltima = function (SensorName, Interval) {
        var response = $scope.callAPI($scope.base_url_api, 'GET', SensorName, Interval, 1, 0);
        try {
            console.log(response);
            //Only get first one in case of too many datasets
            return response[0];
        } catch (err) {
            console.log("Error in createSensorObjects/getSensorIntervalUltima:" + err);
        }
    }

    //Get Current Temp
    $scope.getSensorCurrentTemp = function (SensorName) {
        var response = $scope.callAPI($scope.base_url_api, 'GET', SensorName, 1, 1, 0);
        try {
            //Only get first one in case of too many datasets
            return response[0].avg_temperature;
        } catch (err) {
            console.log("Error in createSensorObjects/getSensorCurrentTemp:" + err);
        }
    }



    //API Calls %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    $scope.getSensorList = function () {


        var CompleteUrl = $scope.base_url_api + '/targets';
        //example response: '[{"name":"sensor0","threshold":32.0},{"name":"sensor1","threshold":31.0},{"name":"sensor2","threshold":40.0}]';

        /*
        var parsedResponse = JSON.parse('[{"name":"sensor0","threshold":32.0},{"name":"sensor1","threshold":31.0},{"name":"sensor2","threshold":40.0}]');
        console.log(parsedResponse);
        $scope.SensorList = parsedResponse;
        $scope.createSensorObjects();
        */


        $http({
            method: 'GET',
            url: CompleteUrl,
            headers: {
                'Content-Type': 'json'
            },
        }).then(function successCallback(response) {
            try {
                $scope.SensorList = response.data;
                $scope.createSensorObjects();
                return response;
            }
            catch (err) {
                console.log("Error while parsing: " + err);
                return null;
            }
        }, function errorCallback(response) {
            console.log(response);
            return null;
        });

    }

    //url example: http://server.fireplace.spankmewithcat6.de/v1/api/stats/client?interval=1&latest=1&offset=0
    // method = GET/POST (string), sensorName(string), interval,later,offset 1,1,0
    $scope.callAPI = function (base_url, method, sensorName, interval, latest, offset) {

        var CompleteUrl = base_url + '/stats/' + sensorName + '?interval=' + interval + '&latest=' + latest + '&offset=' + offset;
        //return '[{"time":"2019-09-07T18:12:50+00:00","min_temperature":33.06,"max_temperature":33.06,"avg_temperature":33.06},{"time":"2019-09-07T18:13:50+20:00","min_temperature":33.06,"max_temperature":33.06,"avg_temperature":33.06},{"time":"2019-09-07T18:14:50+03:00","min_temperature":33.06,"max_temperature":33.06,"avg_temperature":33.06}]';

        var request = new XMLHttpRequest();
        request.open(method, CompleteUrl, false);  // `false` makes the request synchronous
        request.send(null);

        // console.log(request.responseText);
        // debugger;

        return JSON.parse(request.responseText)

        // $http({
        // 	method: method,
        // 	url: CompleteUrl,
        // 	headers: {
        // 		'Content-Type': 'json'
        // 	},
        // }).then(function successCallback(response) {
        // 	return response;
        // }, function errorCallback(response) {
        // 	console.log(response);
        // 	return null;
        // });

    }

    //End API Calls %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    //wait until canvas are created
    window.onload = function () {
        $scope.updateGraphs();
    }//onload end


    $scope.updateGraphs = function () {
        $scope.SensorData.forEach(function (Sensor) {
            console.log("SENSOR:");
            console.log(Sensor);
            //assign each sensorcanvas the data
            var ctx = document.getElementById('Canvas' + Sensor.ID).getContext('2d');
            var chart = new Chart(ctx, {
                //The type of chart we want to create
                type: 'line',

                //The data for our dataset
                data: {
                    labels: Sensor.TTStamps.map(a => a.Time),
                    datasets: [
                        {
                            label: 'Temperaturverlauf ' + Sensor.Name,
                            backgroundColor: 'rgba(0, 123, 255, 0.3)',
                            borderColor: 'rgb(0, 123, 255)',
                            data: Sensor.TTStamps.map(a => a.AvgTemp)
                        }
                    ]
                },

                //Configuration options go here
                options: {
                    //Draw Lines for Avg/Max/Min Temp (needs chartjs annotation plugin)
                    annotation: {
                        annotations: [
                            {
                                type: 'line',
                                mode: 'horizontal',
                                scaleID: 'y-axis-0',
                                value: Sensor.UltAvgTemp,
                                borderColor: 'green',
                                borderWidth: 4
                            },
                            {
                                type: 'line',
                                mode: 'horizontal',
                                scaleID: 'y-axis-0',
                                value: Sensor.AlertMaxTemp,
                                borderColor: 'red',
                                borderWidth: 4
                            }
                            /*,
                            {
                                type: 'line',
                                mode: 'horizontal',
                                scaleID: 'y-axis-0',
                                value: Sensor.AlertMinTemp,
                                borderColor: 'rgb(0, 187, 255)',
                                borderWidth: 4
                            }*/
                        ]
                    }
                }
            });//chart end

            //alert cases (add more?)
            if (Sensor.CurrentTemp > Sensor.AlertMaxTemp) {
                var CardHeader = document.getElementById('cardheader' + Sensor.ID);
                if (CardHeader != null) {
                    CardHeader.style.backgroundColor = "rgb(206, 48, 41)    ";
                    console.log("changed color of " + Sensor.ID);
                } else {
                    console.log("cardheader" + Sensor.ID + " is null");
                }
            }
            if (Sensor.CurrentTemp < Sensor.AlertMinTemp) {
                var CardHeader = document.getElementById('cardheader' + Sensor.ID);
                if (CardHeader != null) {
                    CardHeader.style.backgroundColor = "rgb(0, 187, 255)";
                    console.log("changed color of " + Sensor.ID);
                } else {
                    console.log("cardheader" + Sensor.ID + " is null");
                }
            }
        })//foreach end
    }

    $scope.refreshData = function() {
        $scope.SensorData.forEach(sensor => {
            console.log("refreshing")
            sensor.mod()
        })
    }



    //Main Call ###################################################
    $scope.getSensorList();

    window.setInterval($scope.refreshData, 5000);

    //End Main ###################################################
    //setTimeout(h =>  $scope.$apply(), 1000);


})
