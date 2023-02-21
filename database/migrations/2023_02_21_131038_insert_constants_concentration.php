<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class InsertConstantsConcentration extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        DB::table('constants')->insert(['name' => 'min_i_particulate', 'constant' => '4000']);
        DB::table('constants')->insert(['name' => 'max_i_particulate', 'constant' => '20000']);
        DB::table('constants')->insert(['name' => 'min_particulate', 'constant' => '0']);
        DB::table('constants')->insert(['name' => 'max_particulate', 'constant' => '350']);
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        //
    }
}
