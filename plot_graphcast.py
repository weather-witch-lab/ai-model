import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import os
import pandas as pd

class WeatherPlotter:
    def __init__(self, output_base='weather_plots'):
        self.output_base = output_base
        self.plot_types = {
            'temperature': self.plot_temperature,
            'wind': self.plot_wind,
            'pressure': self.plot_pressure,
            'combined': self.plot_combined
        }

    def setup_output_directory(self, subdir):
        output_dir = os.path.join(self.output_base, subdir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    def create_base_map(self, figsize=(15, 10)):
        fig = plt.figure(figsize=figsize)
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
        ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
        return fig, ax

    def plot_temperature(self, ds, timestep, output_dir):
        """Plot 2m temperature map."""
        try:
            # Get 2m temperature data
            ds_t2m = xr.open_dataset('graphcast.grib', engine='cfgrib',
                                   backend_kwargs={'filter_by_keys': {
                                       'typeOfLevel': 'heightAboveGround',
                                       'level': 2
                                   }})
            
            temp = ds_t2m['t2m'].isel(step=timestep) - 273.15  # Convert to Celsius
            
            fig, ax = self.create_base_map()
            
            # Plot temperature
            levels = np.arange(-40, 41, 2)
            cf = ax.contourf(temp.longitude, temp.latitude, temp,
                           levels=levels, cmap='RdBu_r',
                           transform=ccrs.PlateCarree(),
                           extend='both')
            
            plt.colorbar(cf, label='Temperature (°C)', orientation='horizontal',
                        pad=0.05, aspect=50)
            
            timestamp = pd.Timestamp(ds_t2m.valid_time[timestep].values)
            plt.title(f'2m Temperature Forecast\n{timestamp.strftime("%Y-%m-%d %H:%M UTC")}',
                     pad=20)
            
            filename = f'temp_{timestep:03d}_{timestamp.strftime("%Y%m%d_%H%M")}.png'
            plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
            plt.close()
            ds_t2m.close()
            
        except Exception as e:
            print(f"Error plotting temperature for timestep {timestep}: {str(e)}")
            plt.close()

    def plot_wind(self, ds, timestep, output_dir):
        """Plot 10m wind map."""
        try:
            # Get 10m wind data
            ds_wind = xr.open_dataset('graphcast.grib', engine='cfgrib',
                                    backend_kwargs={'filter_by_keys': {
                                        'typeOfLevel': 'heightAboveGround',
                                        'level': 10
                                    }})
            
            u10 = ds_wind['u10'].isel(step=timestep)
            v10 = ds_wind['v10'].isel(step=timestep)
            
            # Calculate wind speed
            wind_speed = np.sqrt(u10**2 + v10**2)
            
            fig, ax = self.create_base_map()
            
            # Plot wind speed
            levels = np.arange(0, 31, 2)
            cf = ax.contourf(wind_speed.longitude, wind_speed.latitude, wind_speed,
                           levels=levels, cmap='viridis',
                           transform=ccrs.PlateCarree(),
                           extend='max')
            
            # Add wind barbs (subset for clarity)
            skip = 20  # Plot every 20th point
            ax.barbs(u10.longitude[::skip], u10.latitude[::skip],
                    u10.values[::skip, ::skip], v10.values[::skip, ::skip],
                    transform=ccrs.PlateCarree(), length=4,
                    sizes=dict(emptybarb=0), alpha=0.6)
            
            plt.colorbar(cf, label='Wind Speed (m/s)', orientation='horizontal',
                        pad=0.05, aspect=50)
            
            timestamp = pd.Timestamp(ds_wind.valid_time[timestep].values)
            plt.title(f'10m Wind Forecast\n{timestamp.strftime("%Y-%m-%d %H:%M UTC")}',
                     pad=20)
            
            filename = f'wind_{timestep:03d}_{timestamp.strftime("%Y%m%d_%H%M")}.png'
            plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
            plt.close()
            ds_wind.close()
            
        except Exception as e:
            print(f"Error plotting wind for timestep {timestep}: {str(e)}")
            plt.close()

    def plot_pressure(self, ds, timestep, output_dir):
        """Plot mean sea level pressure map."""
        try:
            # Get pressure data
            ds_msl = xr.open_dataset('graphcast.grib', engine='cfgrib',
                                   backend_kwargs={'filter_by_keys': {
                                       'typeOfLevel': 'meanSea'
                                   }})
            
            msl = ds_msl['msl'].isel(step=timestep) / 100  # Convert to hPa
            
            fig, ax = self.create_base_map()
            
            # Plot pressure contours
            levels = np.arange(960, 1041, 4)
            cs = ax.contour(msl.longitude, msl.latitude, msl,
                          levels=levels, colors='black',
                          transform=ccrs.PlateCarree())
            ax.clabel(cs, inline=True, fmt='%d')
            
            timestamp = pd.Timestamp(ds_msl.valid_time[timestep].values)
            plt.title(f'Mean Sea Level Pressure Forecast\n{timestamp.strftime("%Y-%m-%d %H:%M UTC")}',
                     pad=20)
            
            filename = f'pressure_{timestep:03d}_{timestamp.strftime("%Y%m%d_%H%M")}.png'
            plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
            plt.close()
            ds_msl.close()
            
        except Exception as e:
            print(f"Error plotting pressure for timestep {timestep}: {str(e)}")
            plt.close()

    def plot_combined(self, ds, timestep, output_dir):
        """Plot combined weather map."""
        try:
            # Get all required data
            ds_t2m = xr.open_dataset('graphcast.grib', engine='cfgrib',
                                   backend_kwargs={'filter_by_keys': {
                                       'typeOfLevel': 'heightAboveGround',
                                       'level': 2
                                   }})
            
            ds_wind = xr.open_dataset('graphcast.grib', engine='cfgrib',
                                    backend_kwargs={'filter_by_keys': {
                                        'typeOfLevel': 'heightAboveGround',
                                        'level': 10
                                    }})
            
            ds_msl = xr.open_dataset('graphcast.grib', engine='cfgrib',
                                   backend_kwargs={'filter_by_keys': {
                                       'typeOfLevel': 'meanSea'
                                   }})
            
            temp = ds_t2m['t2m'].isel(step=timestep) - 273.15
            u10 = ds_wind['u10'].isel(step=timestep)
            v10 = ds_wind['v10'].isel(step=timestep)
            msl = ds_msl['msl'].isel(step=timestep) / 100
            
            fig, ax = self.create_base_map(figsize=(18, 12))
            
            # Plot temperature
            levels_temp = np.arange(-40, 41, 2)
            cf = ax.contourf(temp.longitude, temp.latitude, temp,
                           levels=levels_temp, cmap='RdBu_r',
                           transform=ccrs.PlateCarree(), alpha=0.7)
            
            # Add pressure contours
            cs = ax.contour(msl.longitude, msl.latitude, msl,
                          levels=np.arange(960, 1041, 4),
                          colors='black', alpha=0.6,
                          transform=ccrs.PlateCarree())
            ax.clabel(cs, inline=True, fmt='%d')
            
            # Add wind barbs
            skip = 20
            ax.barbs(u10.longitude[::skip], u10.latitude[::skip],
                    u10.values[::skip, ::skip], v10.values[::skip, ::skip],
                    transform=ccrs.PlateCarree(), length=4,
                    sizes=dict(emptybarb=0), alpha=0.6)
            
            plt.colorbar(cf, label='Temperature (°C)', orientation='horizontal',
                        pad=0.05, aspect=50)
            
            timestamp = pd.Timestamp(ds_t2m.valid_time[timestep].values)
            plt.title(f'Combined Weather Forecast\n{timestamp.strftime("%Y-%m-%d %H:%M UTC")}',
                     pad=20)
            
            filename = f'combined_{timestep:03d}_{timestamp.strftime("%Y%m%d_%H%M")}.png'
            plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
            plt.close()
            
            # Close all datasets
            ds_t2m.close()
            ds_wind.close()
            ds_msl.close()
            
        except Exception as e:
            print(f"Error plotting combined map for timestep {timestep}: {str(e)}")
            plt.close()

    def process_grib_file(self, grib_file, plot_types=None):
        """Process GRIB file and create all requested plot types."""
        if plot_types is None:
            plot_types = ['combined']
            
        print(f"\nProcessing GRIB file: {grib_file}")
        
        try:
            # Create output directories
            for plot_type in plot_types:
                self.setup_output_directory(plot_type)
            
            # Process each timestep
            for i in range(41):  # We confirmed there are 41 timesteps
                print(f"\nProcessing timestep {i+1}/41")
                
                # Create each requested plot type
                for plot_type in plot_types:
                    if plot_type in self.plot_types:
                        print(f"Creating {plot_type} plot...")
                        output_dir = os.path.join(self.output_base, plot_type)
                        self.plot_types[plot_type](None, i, output_dir)  # Pass None as ds since we open specific datasets in each plot function
                    else:
                        print(f"Unknown plot type: {plot_type}")
                
        except Exception as e:
            print(f"Error processing file: {str(e)}")

def main():
    # Initialize plotter
    plotter = WeatherPlotter()
    
    # Process GRIB file with all plot types
    plotter.process_grib_file('graphcast.grib',
                             plot_types=['temperature', 'wind', 'pressure', 'combined'])

if __name__ == "__main__":
    main()