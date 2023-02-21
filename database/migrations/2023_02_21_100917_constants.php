<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class Constants extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('constants', function (Blueprint $table) {
            $table->id();
            $table->string('name')->nullable();
            $table->string('constant')->nullable();
            $table->timestamps();
        });

        DB::table('constants')->insert(['name' => 'A', 'constant' => '-0.079']);
        DB::table('constants')->insert(['name' => 'B', 'constant' => '22.245']);
        DB::table('constants')->insert(['name' => 'C', 'constant' => '-2.2']);
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('constants');
    }
}
