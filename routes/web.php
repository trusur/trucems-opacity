<?php

/** @var \Laravel\Lumen\Routing\Router $router */

use App\Http\Controllers\ExampleController;

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It is a breeze. Simply tell Lumen the URIs it should respond to
| and give it the Closure to call when that URI is requested.
|
*/

$router->get('/', 'DashboardController@index');
$router->get('/quality-standards', 'DashboardController@qualityStandard');
$router->get('/configurations', 'ConfigurationController@index');
$router->patch('/configurations', 'ConfigurationController@update');
$router->get('/sensors', 'SensorController@index');
$router->group(['prefix' => 'sensor'], function () use ($router) {
    $router->get('/edit/{sensorId}', 'SensorController@edit');
    $router->patch('/update/{sensorId}', 'SensorController@update');
});

/**
 * API
 */
$router->group(['prefix' => 'api'], function () use ($router) {
     /**
     * Sensor Value Logs
     */
    $router->patch('/sensor-value/{sensorId}', 'API\ValueLogsController@update');
    $router->get('/sensor-value-logs', 'API\ValueLogsController@index');

    /**
     * List Sensors
     */
    $router->get('/sensor-lists', 'API\SensorsController@index');
    $router->get('/sensor-value/{sensorId}', 'API\SensorsController@getById');

    $router->get('/runtime', 'API\RuntimeController@index');
    $router->patch('/runtime', 'API\RuntimeController@store');
});
