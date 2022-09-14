<?php

namespace Database\Seeders;

use App\Models\Sensor;
use App\Models\SensorValue;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Schema;

class SensorSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        Schema::disableForeignKeyConstraints();
        Sensor::truncate();
        Sensor::insert([
            [
                'unit_id' => 1,
                'code' => 'opacity',
                'name' => 'Opacity',
                'read_formula' => 'round((0.00625 * value) - 25, 3)',
                'write_address' => '0', //ch3
            ],
        ]);
        SensorValue::insert([
            'sensor_id' => 1,
            'value' => 0
        ]);
    }
}
