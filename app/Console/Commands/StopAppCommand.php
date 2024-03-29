<?php

namespace App\Console\Commands;

use App\Models\Configuration;
use Illuminate\Console\Command;

class StopAppCommand extends Command
{
    protected $signature = 'stop-app';
    protected $description = 'Command for app closed';

    public function handle()
    {
        Configuration::find(1)->update([
            'is_calibration' => 0,
            'date_and_time' => date('Y-m-d H:i:s')
        ]);
    }
   
}
